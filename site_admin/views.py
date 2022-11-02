from django.shortcuts import render, redirect
import requests
from django.views.generic import TemplateView
from django.core.exceptions import PermissionDenied
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.messages.views import SuccessMessageMixin, messages
from django.core.mail import EmailMessage, send_mail
from django.views.generic.detail import DetailView
from django.template import RequestContext
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Q, Sum
from datetime import date, datetime, timedelta
from django.shortcuts import get_object_or_404
from twilio.rest import Client
from django.conf import settings
from site_setup.models import SiteSetupModel


class AdminDashboardView(TemplateView):
    template_name = 'site_admin/dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


def format_phone_number(phone_number_list):
    clean_list = ''
    for index, phone_number in enumerate(phone_number_list):
        phone_number = str(phone_number)
        if len(phone_number) == 10:
            if phone_number[0] == '0':
                return False
            phone_number = '234' + phone_number
            if index != (len(phone_number_list) - 1):
                clean_list += phone_number + ','
            else:
                clean_list += phone_number
        elif len(phone_number) == 11:
            if phone_number[0] != '0':
                return False
            phone_number = '234' + phone_number[1:]
            if index != (len(phone_number_list) - 1):
                clean_list += phone_number + ','
            else:
                clean_list += phone_number
        if clean_list:
            return clean_list
        return False



def send_sms(sender, reciever, message):
    reciever = format_phone_number(reciever)
    if reciever:
        url = 'https://www.bulksmsnigeria.com/api/v1/sms/create'
        
        params = {
          'api_token': settings.SMS_API,
          'to': reciever,
          'from': sender,
          'body': message,
          'gateway': '0',
          'append_sender': '0',
        }
        headers = {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        }

        response = requests.request('POST', url, headers=headers, params=params)
        response.json()

        # account_sid = settings.TWILIO_SID
        # auth_token = settings.TWILIO_AUTH_TOKEN
        # sender = settings.TWILIO_PHONE_NUMBER
        
        # client = Client(account_sid, auth_token)
        # message = client.messages.create(to=reciever, from_=sender, body=message)
        
        
        
def send_admin_mail(request):
    if request.method == 'POST':
        full_name = request.POST['full_name']
        mobile = request.POST['mobile']
        message = request.POST['message']
        
        site_info = SiteSetupModel.objects.first()

        # send mail to client and supplier
        context = {
            'domain': get_current_site(request),
            'site_info': site_info,
            'message': message,
            'mobile': mobile,
            'full_name': full_name
        }
        
        mail_subject = 'mesaage from {}'.format(full_name)
        from_email = settings.EMAIL_HOST_USER
        html_message = render_to_string('home/mail/to_admin.html', context)
        plain_message = strip_tags(html_message)
        to_mail = [site_info.email]
        
        mail_sent = send_mail(mail_subject, html_message, from_email, to_mail,
                              html_message=html_message,
                              fail_silently=True)
        if mail_sent:
            messages.success(request, 'Message Sent')
        else:
            messages.success(request, 'Failed to send Message, Try Later')
        return redirect(reverse('contact'))
    raise PermissionDenied()
    
    
import requests
import json


