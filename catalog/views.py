from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.contrib.messages.views import SuccessMessageMixin, messages
from django.views.generic.detail import DetailView
from django.template import RequestContext
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Q, Sum
from datetime import date, datetime, timedelta
from django.shortcuts import get_object_or_404
from catalog.models import *
from catalog.forms import *


class CategoryCreateView(SuccessMessageMixin, CreateView):
    model = CategoryModel
    form_class = CategoryForm
    template_name = 'catalog/category/index.html'
    success_message = 'Product Category Added Successfully'

    def get_success_url(self):
        return reverse('category_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CategoryListView(ListView):
    model = CategoryModel
    fields = '__all__'
    template_name = 'catalog/category/index.html'
    context_object_name = "category_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CategoryForm()
        return context


class CategoryUpdateView(SuccessMessageMixin, UpdateView):
    model = CategoryModel
    form_class = CategoryForm
    template_name = template_name = 'catalog/category/index.html'
    success_message = 'Product Category Successfully Updated'

    def get_success_url(self):
        return reverse('category_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CategoryDeleteView(DeleteView):
    model = CategoryModel
    template_name = 'catalog/category/delete.html'
    context_object_name = "category"

    def get_success_url(self):
        return reverse('category_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProductSizeCreateView(SuccessMessageMixin, CreateView):
    model = ProductSizeModel
    form_class = ProductSizeForm
    template_name = 'catalog/size/index.html'
    success_message = 'Product Size Added Successfully'

    def get_success_url(self):
        return reverse('size_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProductSizeListView(ListView):
    model = ProductSizeModel
    fields = '__all__'
    template_name = 'catalog/size/index.html'
    context_object_name = "product_size_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProductSizeForm
        return context


class ProductSizeUpdateView(SuccessMessageMixin, UpdateView):
    model = ProductSizeModel
    form_class = ProductSizeForm
    template_name = template_name = 'catalog/size/index.html'
    success_message = 'Product Size Successfully Updated'

    def get_success_url(self):
        return reverse('size_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProductSizeDeleteView(DeleteView):
    model = ProductSizeModel
    template_name = 'catalog/size/delete.html'
    context_object_name = "product_size"

    def get_success_url(self):
        return reverse('size_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProductCreateView(SuccessMessageMixin, CreateView):
    model = ProductModel
    form_class = ProductForm
    template_name = 'catalog/product/index.html'
    success_message = 'Product Added Successfully'

    def get_success_url(self):
        return reverse('product_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProductListView(ListView):
    model = ProductModel
    fields = '__all__'
    template_name = 'catalog/product/index.html'
    context_object_name = "product_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProductForm
        context['category_list'] = CategoryModel.objects.order_by('title')
        return context


class ProductUpdateView(SuccessMessageMixin, UpdateView):
    model = ProductModel
    form_class = ProductForm
    template_name = 'catalog/product/index.html'
    success_message = 'Product Successfully Updated'

    def get_success_url(self):
        return reverse('product_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProductDetailView(SuccessMessageMixin, DetailView):
    model = ProductModel
    context_object_name = 'product'
    template_name = 'catalog/product/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProductVariantForm
        context['size_list'] = ProductSizeModel.objects.order_by('size')
        return context


class ProductDeleteView(DeleteView):
    model = ProductModel
    template_name = 'catalog/product/delete.html'
    context_object_name = "product"

    def get_success_url(self):
        return reverse('product_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProductVariantCreateView(SuccessMessageMixin, CreateView):
    model = ProductVariantModel
    form_class = ProductVariantForm
    template_name = 'catalog/product_variant/index.html'
    success_message = 'Product Variant Added Successfully'

    def get_success_url(self):
        return reverse('product_detail', kwargs={'pk':self.object.product.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProductVariantListView(ListView):
    model = ProductVariantModel
    fields = '__all__'
    template_name = 'catalog/product_variant/index.html'
    context_object_name = "variant_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProductVariantForm
        return context


class ProductVariantUpdateView(SuccessMessageMixin, UpdateView):
    model = ProductVariantModel
    form_class = ProductVariantForm
    template_name = 'catalog/product_variant/index.html'
    success_message = 'Product Variant Successfully Updated'

    def get_success_url(self):
        return reverse('product_detail', kwargs={'pk': self.object.product.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProductVariantDetailView(SuccessMessageMixin, DetailView):
    model = ProductVariantModel
    template_name = 'catalog/product_variant/detail.html'
    context_object_name = 'variant'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProductVariantDeleteView(DeleteView):
    model = ProductVariantModel
    template_name = 'catalog/product_variant/delete.html'
    context_object_name = "variant"

    def get_success_url(self):
        return reverse('variant_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
