# cart/views.py
from django.shortcuts import render, redirect, get_object_or_404
from shop.models import Product
from .models import Cart, CartItem

# ----- Helper Function -----
def _get_or_create_cart(request):
    """Get or create a cart for the current user/session"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart

# ----- Cart Views -----
def cart_detail(request):
    try:
        cart = _get_or_create_cart(request)
        cart_items = cart.items.all()  # Use related_name 'items'
        total = sum(item.subtotal() for item in cart_items)
        counter = sum(item.quantity for item in cart_items)
    except Cart.DoesNotExist:
        cart_items = []
        total = 0
        counter = 0
    
    return render(request, 'cart/cart.html', {
        'cart_items': cart_items,
        'total': total,
        'counter': counter
    })
    
from django.db import transaction

def add_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    
    # Get or create cart
    cart = _get_or_create_cart(request)
    
    # Update or create cart item
    with transaction.atomic():  # Prevent race conditions
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
    
    return redirect('cart:cart_detail')
# ... keep remove_cart and full_remove views as before ...

def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id=_get_or_create_cart(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
        
    return redirect('cart:cart_detail')

def full_remove(request, product_id):
    cart = Cart.objects.get(cart_id=_get_or_create_cart(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart:cart_detail')