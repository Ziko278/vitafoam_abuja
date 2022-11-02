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
from site_setup.models import SiteSetupModel, SiteHeroModel
from site_setup.forms import SiteSetupForm, SiteHeroForm


class SiteInfoView(TemplateView):
    template_name = 'site_setup/site_info/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site_info = SiteSetupModel.objects.first()
        if not site_info:
            form = SiteSetupForm()
            is_site_info = False
        else:
            form = SiteSetupForm(instance=site_info)
            is_site_info = True
        context['form'] = form
        context['is_site_info'] = is_site_info
        context['site_info'] = site_info
        return context


class SiteInfoCreateView(SuccessMessageMixin, CreateView):
    model = SiteSetupModel
    form_class = SiteSetupForm
    template_name = 'site_setup/site_info/index.html'
    success_message = 'Site Info updated Successfully'

    def get_success_url(self):
        return reverse('site_info')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SiteInfoUpdateView(SuccessMessageMixin, UpdateView):
    model = SiteSetupModel
    form_class = SiteSetupForm
    template_name = 'site_setup/site_info/index.html'
    success_message = 'Site Info updated Successfully'

    def get_success_url(self):
        return reverse('site_info')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SiteHeroCreateView(SuccessMessageMixin, CreateView):
    model = SiteHeroModel
    form_class = SiteHeroForm
    template_name = 'site_setup/hero/index.html'
    success_message = 'Website Banner Added Successfully'

    def get_success_url(self):
        return reverse('banner_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SiteHeroListView(ListView):
    model = SiteHeroModel
    fields = '__all__'
    template_name = 'site_setup/hero/index.html'
    context_object_name = "website_banner_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SiteHeroForm()
        return context


class SiteHeroUpdateView(SuccessMessageMixin, UpdateView):
    model = SiteHeroModel
    form_class = SiteHeroForm
    template_name = template_name = 'site_setup/hero/index.html'
    success_message = 'Website Banner Successfully Updated'

    def get_success_url(self):
        return reverse('banner_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SiteHeroDeleteView(DeleteView):
    model = SiteHeroModel
    template_name = 'site_setup/hero/delete.html'
    context_object_name = "banner"

    def get_success_url(self):
        return reverse('banner_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
