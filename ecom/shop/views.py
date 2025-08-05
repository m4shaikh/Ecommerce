from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.decorators import seller_required
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

from django.shortcuts import get_object_or_404

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
        
    return render(request, 'shop/product/list.html', {
        'category': category,
        'categories': categories,
        'products': products
    })

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    return render(request, 'shop/product/detail.html', {'product': product})