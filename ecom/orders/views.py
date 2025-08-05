from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
import stripe
import logging
from cart.models import Cart, CartItem
from shop.models import Product
from .models import Order, OrderItem
from .forms import OrderCreateForm

# Initialize Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

# Logger
logger = logging.getLogger(__name__)

# ----- Helper Functions -----
def _cart_id(request):
    """Get or create session-based cart ID."""
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key

def _get_or_create_cart(request):
    """Get or create a cart for the current user/session."""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = _cart_id(request)
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart

# ----- Order Views -----
def order_create(request):
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)  # Bind form to POST data
    else:
        # Pre-fill form for logged-in users
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'full_name': request.user.get_full_name(),
                'email': request.user.email,
                'email_confirmation': request.user.email,
                'address': request.user.address,
                'phone': request.user.phone_number,
            }
        form = OrderCreateForm(initial=initial_data)  # Pre-fill form

    try:
        cart = _get_or_create_cart(request)
        cart_items = CartItem.objects.filter(cart=cart)

        if not cart_items.exists():
            return redirect('cart:cart_detail')

        if request.method == 'POST':
            if form.is_valid():
                with transaction.atomic():
                    # Create order
                    order = form.save(commit=False)
                    if request.user.is_authenticated:
                        order.user = request.user
                    order.save()

                    # Create order items and reserve stock
                    for item in cart_items:
                        if item.product.stock >= item.quantity:
                            OrderItem.objects.create(
                                order=order,
                                product=item.product,
                                price=item.product.price,
                                quantity=item.quantity
                            )
                            item.product.stock -= item.quantity  # Reserve stock
                            item.product.save()
                            item.delete()  # Remove item from cart
                        else:
                            logger.error(f"Insufficient stock for product {item.product.id}")
                            return render(request, 'orders/stock_error.html', {'product': item.product})

                    # Store order ID in session
                    request.session['order_id'] = order.id
                    request.session.modified = True

                    # Clear cart from session (if it exists)
                    if 'cart_id' in request.session:
                        del request.session['cart_id']
                
                    # Redirect to payment
                    return redirect('orders:payment_process')

        total = sum(item.product.price * item.quantity for item in cart_items)
        return render(request, 'orders/create.html', {
            'form': form,
            'cart_items': cart_items,
            'total': total
        })

    except Cart.DoesNotExist:
        return redirect('shop:product_list')
    
def payment_process(request):
    """Process payment via Stripe."""
    order_id = request.session.get('order_id')
    if not order_id:
        return redirect('shop:product_list')
    
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        try:
            success_url = request.build_absolute_uri(
                reverse('orders:payment_completed')
            )
            cancel_url = request.build_absolute_uri(
                reverse('orders:payment_canceled')
            )
            
            session_data = {
                'mode': 'payment',
                'client_reference_id': order.id,
                'success_url': success_url,
                'cancel_url': cancel_url,
                'line_items': []
            }
            
            for item in order.items.all():
                session_data['line_items'].append({
                    'price_data': {
                        'unit_amount': int(item.price * 100),
                        'currency': settings.DEFAULT_CURRENCY,
                        'product_data': {'name': item.product.name},
                    },
                    'quantity': item.quantity,
                })
            
            session = stripe.checkout.Session.create(**session_data)
            order.stripe_id = session.payment_intent  # Use PaymentIntent ID
            order.save()
            
            return redirect(session.url, code=303)
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error: {str(e)}")
            return render(request, 'orders/payment_error.html', {'error': str(e)})
    
    return render(request, 'orders/payment_process.html', {'order': order})

def payment_completed(request):
    """Display payment success page."""
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/payment_completed.html', {'order': order})

def payment_canceled(request):
    """Display payment cancellation page."""
    return render(request, 'orders/payment_canceled.html')

# ----- Webhook Handlers -----
@csrf_exempt
def stripe_webhook(request):
    """Handle Stripe webhook events."""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        logger.error("Invalid payload")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        logger.error("Invalid signature")
        return HttpResponse(status=400)

    if event.type == 'checkout.session.completed':
        session = event.data.object
        try:
            handle_checkout_session(session)
        except Exception as e:
            logger.error(f"Error handling checkout session: {str(e)}")
            return HttpResponse(status=500)
    
    return HttpResponse(status=200)

def handle_checkout_session(session):
    """Handle successful payment via Stripe webhook."""
    try:
        order = Order.objects.get(id=session.client_reference_id)
        
        # Prevent duplicate processing
        if order.paid:
            logger.warning(f"Order {order.id} already marked as paid")
            return
        
        # Mark order as paid
        order.paid = True
        order.stripe_id = session.payment_intent
        order.save()
        
        # Send confirmation email
        subject = f"Order #{order.id} Confirmation"
        message = render_to_string('orders/email/order_confirmation.txt', {'order': order})
        html_message = render_to_string('orders/email/order_confirmation.html', {'order': order})
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [order.email],
            html_message=html_message
        )
        
    except Order.DoesNotExist:
        logger.error(f"Order not found: {session.client_reference_id}")
        raise
    except Exception as e:
        logger.error(f"Error processing order {session.client_reference_id}: {str(e)}")
        raise