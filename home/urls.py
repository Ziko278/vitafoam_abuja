from django.urls import path
from home.views import *
from site_admin.views import send_admin_mail
from order.views import PayWithPaystackView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('shop/<str:filter>', ShopView.as_view(), name='shop'),
    path('shop/search/<str:search>', ShopSearchView.as_view(), name='search'),
    path('shop/product/pre-search', pre_search_view, name='pre-search'),
    path('shop/product/<int:pk>/detail', ShopDetailView.as_view(), name='shop-detail'),
    path('about', AboutPageView.as_view(), name='about'),
    path('contact-us', ContactView.as_view(), name='contact'),
    path('message/send', send_admin_mail, name='send_admin_mail'),


]

