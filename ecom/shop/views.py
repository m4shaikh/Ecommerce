
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.decorators import seller_required
from django.db.models import Q
import random
from .models import Product, Category
from .forms import ProductForm

@login_required
@seller_required
def seller_dashboard(request):
    products = Product.objects.filter(seller=request.user)
    return render(request, 'shop/seller/dashboard.html', {
        'products': products,
        'categories': Category.objects.all()
    })

@login_required
@seller_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect('shop:seller_dashboard')
    else:
        form = ProductForm()
    return render(request, 'shop/seller/product_form.html', {'form': form})

@login_required
@seller_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('shop:seller_dashboard')
    else:
        form = ProductForm(instance=product)
    return render(request, 'shop/seller/product_form.html', {'form': form})

@login_required
@seller_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == 'POST':
        product.delete()
        return redirect('shop:seller_dashboard')
    return render(request, 'shop/seller/product_confirm_delete.html', {'product': product})

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    
    # Category filter
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    # Search query
    search_query = request.GET.get('q', '').strip()
    if search_query:
        products = products.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))

    # Price range filter
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    # In stock only filter
    in_stock = request.GET.get('in_stock')
    if in_stock:
        products = products.filter(stock__gt=0)

    # Sorting & Randomization
    sort_by = request.GET.get('sort', '')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'newest':
        products = products.order_by('-created')
    else:
        # Default: Randomize products on grid if no specific sort or search is applied
        products = list(products)
        random.shuffle(products)

    return render(request, 'shop/product/list.html', {
        'category': category,
        'categories': categories,
        'products': products,
        'search_query': search_query,
        'min_price': min_price,
        'max_price': max_price,
        'in_stock': in_stock,
        'sort_by': sort_by,
    })

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    return render(request, 'shop/product/detail.html', {'product': product})


@login_required
@seller_required
def category_create(request):
    next_url = request.GET.get('next') or request.POST.get('next')

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            if next_url:
                return redirect(next_url)
            return redirect('shop:seller_dashboard')
    else:
        form = CategoryForm()

    return render(request, 'shop/seller/category_form.html', {
        'form': form,
        'next': next_url
    })