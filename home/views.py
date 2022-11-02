from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.template import RequestContext
from django.http import HttpResponse
from django.urls import reverse
import random
from django.contrib.auth.models import User
from site_setup.models import SiteHeroModel, SiteSetupModel
from catalog.models import *
from email.mime.text import MIMEText


def test(request):
    context = {
        'domain': get_current_site(request)
    }
    return render(request, 'home/mail/admin_order.html', context)
    

class HomePageView(TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['banner_list'] = SiteHeroModel.objects.filter(status='active')[:4]
        context['category_list'] = CategoryModel.objects.all()[:3]
        context['product_list'] = sorted(ProductModel.objects.all(), key=lambda x: random.random())[:15]
        return context
        
    


class ShopView(ListView):
    model = ProductVariantModel
    template_name = 'home/shop.html'
    context_object_name = 'product_list'
    paginate_by = 15

    def get_queryset(self):
        filter = self.kwargs.get('filter')
        if filter == 'all':
            return sorted(ProductModel.objects.all(), key=lambda x: random.random())
        return ProductModel.objects.filter(category__title=filter)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.kwargs.get('filter')
        context['category_list'] = CategoryModel.objects.all()
        return context


def pre_search_view(request):
    search = request.GET['search']
    return redirect(reverse('search', kwargs={'search': search}))


class ShopSearchView(ListView):
    model = ProductVariantModel
    template_name = 'home/search.html'
    context_object_name = 'product_list'
    paginate_by = 15

    def get_queryset(self):
        search = self.kwargs.get('search').strip()
        return sorted(ProductModel.objects.filter(keys__icontains=search), key=lambda x: random.random())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.kwargs.get('search')
        context['category_list'] = CategoryModel.objects.all()

        return context


class ShopDetailView(DetailView):
    model = ProductVariantModel
    template_name = 'home/product_detail.html'
    context_object_name = 'variant'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AboutPageView(TemplateView):
    template_name = 'home/about.html'


class ContactView(TemplateView):
    template_name = 'home/contact.html'


