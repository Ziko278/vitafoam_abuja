from django.urls import path
from order.views import *
from catalog.models import *


urlpatterns = [
    path('cart/make', make_cart_view, name='make_cart'),
    path('cart/product/remove', remove_from_cart_view, name='remove_from_cart'),
    path('cart/check-out', check_out_view, name='check-out'),
    path('cart', cart_view, name='cart'),
    path('check-out/success', checkout_done_view, name='check_out_done'),
    
    
    path('payment/paystack', PayWithPaystackView.as_view(), name='make_payment_paystack'),
    path('payment/paystack/done', verify_paystack_transaction, name='make_payment_paystack_done'),
    # path('wallet/deposit/paystack/payment/webhook', paystack_webhook, name='deposit_webhook'),
]

