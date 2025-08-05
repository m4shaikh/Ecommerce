# orders/urls.py
from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('payment/process/', views.payment_process, name='payment_process'),
    path('payment/completed/', views.payment_completed, name='payment_completed'),
    path('payment/canceled/', views.payment_canceled, name='payment_canceled'),
    path('stripe/webhook/', views.stripe_webhook, name='stripe_webhook'),
]