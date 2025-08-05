from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    # Seller Dashboard URLs
    path('seller/dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('seller/products/add/', views.product_create, name='product_create'),
    path('seller/products/<int:pk>/edit/', views.product_update, name='product_update'),
    path('seller/products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('', views.product_list, name='product_list'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
]