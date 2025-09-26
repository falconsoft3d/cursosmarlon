from django.urls import path
from . import views

urlpatterns = [
    path('carrito/', views.cart_view, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('mis-ordenes/', views.my_orders, name='my_orders'),
    path('pago-exitoso/<int:order_id>/', views.payment_success, name='payment_success'),
    path('api/remove-from-cart/', views.remove_from_cart, name='remove_from_cart'),
    path('api/create-payment-intent/', views.create_payment_intent, name='create_payment_intent'),
    path('api/confirm-payment/', views.confirm_payment, name='confirm_payment'),
    path('api/apply-coupon/', views.apply_coupon, name='apply_coupon'),
]