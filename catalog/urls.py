from django.urls import path
from catalog.views import *


urlpatterns = [
    path('category/register', CategoryCreateView.as_view(), name='category_create'),
    path('category/index', CategoryListView.as_view(), name='category_index'),
    path('category/<int:pk>/edit', CategoryUpdateView.as_view(), name='category_edit'),
    path('category/<int:pk>/delete', CategoryDeleteView.as_view(), name='category_delete'),

    path('size/register', ProductSizeCreateView.as_view(), name='size_create'),
    path('size/index', ProductSizeListView.as_view(), name='size_index'),
    path('size/<int:pk>/edit', ProductSizeUpdateView.as_view(), name='size_edit'),
    path('size/<int:pk>/delete', ProductSizeDeleteView.as_view(), name='size_delete'),

    path('product/register', ProductCreateView.as_view(), name='product_create'),
    path('product/index', ProductListView.as_view(), name='product_index'),
    path('product/<int:pk>/detail', ProductDetailView.as_view(), name='product_detail'),
    path('product/<int:pk>/edit', ProductUpdateView.as_view(), name='product_edit'),
    path('product/<int:pk>/delete', ProductDeleteView.as_view(), name='product_delete'),

    path('product/variant/register', ProductVariantCreateView.as_view(), name='variant_create'),
    path('product/variant/index', ProductVariantListView.as_view(), name='variant_index'),
    path('product/variant/<int:pk>/detail', ProductVariantDetailView.as_view(), name='variant_detail'),
    path('product/variant/<int:pk>/edit', ProductVariantUpdateView.as_view(), name='variant_edit'),
    path('product/variant/<int:pk>/delete', ProductVariantDeleteView.as_view(), name='variant_delete'),

]

