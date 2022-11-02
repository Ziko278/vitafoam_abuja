from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.messages.views import SuccessMessageMixin, messages
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.core.exceptions import PermissionDenied
from django.core.mail import EmailMessage, send_mail
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.exceptions import PermissionDenied
from django.conf import settings
import requests
from django.core.exceptions import ValidationError
import hmac
from ipaddress import ip_address, ip_network
from django.contrib.sites.shortcuts import get_current_site
from django.template import RequestContext
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User
from django.db.models import Q, Sum
from datetime import date, datetime, timedelta
from django.shortcuts import get_object_or_404
from catalog.forms import *
from order.models import *
from site_setup.models import SiteSetupModel
from site_admin.views import send_sms
import random


def make_cart_view(request):
    product_id = request.GET.get('id', None)
    if not product_id:
        return HttpResponse('fail')
    product_id = int(product_id)
    price = request.GET['price']
    price = float(price)
    cart = request.session.get('cart', None)
    cart_price = request.session.get('cart_price', None)
    if not cart:
        request.session['cart'] = []
    if not cart_price:
        cart_price = 0
    cart = request.session['cart']
    if product_id in cart:
        cart.remove(product_id)
        cart_price -= price
        request.session['cart'] = cart
        request.session['cart_price'] = cart_price
        return HttpResponse('removed')

    else:
        cart.append(product_id)
        cart_price += price
        request.session['cart'] = cart
        request.session['cart_price'] = cart_price
        return HttpResponse('added')
        
        
def remove_from_cart_view(request):
    product_id = request.GET.get('id', None)
    if not product_id:
        return HttpResponse('fail')
    product_id = int(product_id)
    price = request.GET['price']
    price = float(price)
    cart = request.session.get('cart', None)
    cart_price = request.session.get('cart_price', None)
    if not cart:
        return HttpResponse('fail')
    cart = request.session['cart']
    if not product_id in cart:
        return HttpResponse('fail')
    else:
        cart.remove(product_id)
        cart_price -= price
        request.session['cart'] = cart
        request.session['cart_price'] = cart_price
        return HttpResponse('removed')


def cart_view(request):
    if request.method == 'POST':
        product_pk_list = request.POST.getlist('product_list[]')
        quantity_list = request.POST.getlist('quantity_list[]')

        total_amount = 0
        product_list = []
        total_price_list = []
        if len(quantity_list) == 0:
            messages.error(request, 'Cart is empty')
            return redirect(reverse('cart'))

        for index, pk in enumerate(product_pk_list):
            product = ProductVariantModel.objects.get(pk=pk)
            product_list.append(product)
            total_amount += (product.price * float(quantity_list[index]))
            total_price_list.append(product.price * float(quantity_list[index]))

        order = OrderModel.objects.create(amount=total_amount, has_paid=False, status='pending', quantity=quantity_list,
                                          price=total_price_list)
        order.save()
        order.products.add(*product_list)
        order.save()

        request.session['order_id'] = order.id
        return redirect(reverse('check-out'))

    cart_pk = request.session.get('cart', None)
    product_list = []
    total_amount = 0
    if cart_pk:
        product_list = ProductVariantModel.objects.filter(pk__in=cart_pk)
        total_amount = product_list.aggregate(Sum('price'))['price__sum']

    context = {
        'product_list': product_list,
        'total_amount': total_amount
    }
    return render(request, 'home/cart.html', context)


def check_out_view(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone')
        email = request.POST.get('email', None)
        delivery_date = request.POST.get('date', datetime.today())

        if not delivery_date:
            delivery_date = datetime.today().date()

        delivery_time = request.POST.get('time')
        if not delivery_time:
            delivery_time = datetime.today().time()

        payment_method = request.POST.get('payment_method')
        order_pk = request.session.get('order_id', None)
        if not order_pk:
            raise PermissionDenied('An Error Occurred')
        order = get_object_or_404(OrderModel, pk=order_pk)
        if order.amount >= 50000:
            transportation = 0
        else:
            transportation = 3000
            
        grand_total = order.amount + transportation

        checkout = CheckOutModel.objects.create(order=order, full_name=full_name, address=address,
                                                mobile=phone_number, email=email, delivery_date=delivery_date,
                                                delivery_time=delivery_time, payment_method=payment_method,
                                                transportation=transportation, grand_total=grand_total)
        checkout.save()
        request.session['checkout_id'] = checkout.id
        site_info = SiteSetupModel.objects.first()

        # send mail to client and supplier
        context = {
            'domain': get_current_site(request),
            'site_info': site_info,
            'checkout': checkout,
        }
        mail_subject = '{} Order Placement'.format(SiteSetupModel.objects.first().name)
        from_email = settings.EMAIL_HOST_USER
        html_message = render_to_string('home/mail/admin_order.html', context)
        plain_message = strip_tags(html_message)
        to_mail = [site_info.email]
        if email:
            to_mail.append(email)
        if payment_method != 'online':
            mail_sent = send_mail(mail_subject, html_message, from_email, to_mail,
                                  html_message=html_message,
                                  fail_silently=True)
            # message admin  
            sms = "Your Order was successfully Placed, Your Order ID is {}. Thank you for choosing {}".format(str(random.randint(100, 999)) + str(checkout.id) + str(random.randint(100, 999)), site_info.name.title())
            message = """An Order was placed successfully"""
            message += """Full Name: {}""".format(full_name)
            message += """Mobile: {}""".format(phone_number)
            message += """Address: {}""".format(address)
            message += """ """
            
            for index, item in enumerate(order.products.all()):
                if item.size:
                    size = '(' + item.size.size + ')'
                else:
                    size = ''
                message += """{} {} ({}) N{}""".format(item.name, size, order.quantity[index], order.price[index])
            message += """Transportation: {}""".format(transportation)
            message += """Total: {}""".format(grand_total)
            message += """Time of Delivery: {} {}""".format(delivery_date, delivery_time)
            
            reciever = [phone_number, site_info.mobile_1]
            sender = site_info.name.upper()
            
            send_sms(sender, reciever, message)
        
        if payment_method == 'delivery':
            return redirect(reverse('check_out_done'))
        else:
            return redirect(reverse('make_payment_paystack'))

    order_pk = request.session.get('order_id', None)
    if not order_pk:
        raise PermissionDenied('An Error Occurred')

    order = get_object_or_404(OrderModel, pk=order_pk)
    if order.amount >= 50000:
        transportation = 0
    else:    
        transportation = 3000
    context = {
        'order': order,
        'transportation': transportation,
        'total': order.amount + transportation
    }

    return render(request, 'home/check_out.html', context)


def make_payment_view(request):
    checkout_id = request.session.get('checkout_id', None)
    if not checkout_id:
        raise PermissionDenied()

    checkout = get_object_or_404(OrderModel, pk=checkout_id)
    del request.session['checkout_id']
    context = {
        'checkout': checkout
    }
    return render(request, 'home/make_payment.html', context)


def checkout_done_view(request):
    checkout_id = request.session.get('checkout_id', None)
    if not checkout_id:
        raise PermissionDenied()

    checkout = get_object_or_404(OrderModel, pk=checkout_id)
    del request.session['checkout_id']
    context = {
        'checkout': checkout
    }
    return render(request, 'home/checkout_done.html', context)

    
    
class PayWithPaystackView(TemplateView):
    template_name = 'home/pay_with_paystack.html'

    def get_context_data(self, **kwargs):
        checkout_id = self.request.session.get('checkout_id', None)
        if not checkout_id:
            raise PermissionDenied()
        
        last_checkout = get_object_or_404(CheckOutModel, pk=checkout_id)
        context = super().get_context_data(**kwargs)
        context['callback_url'] = reverse('make_payment_paystack_done')
        context['last_checkout'] = last_checkout
        context['domain'] = get_current_site(self.request),
 
        context['paystack_secret_key'] = settings.PAY_STACK_TEST_PUBLIC_KEY
        return context


def verify_paystack_transaction(request):
    if 'reference' in request.GET:
        reference = request.GET['reference']
        if request.session['checkout_id']:
            checkout_id = request.session['checkout_id']
            checkout = get_object_or_404(CheckOutModel, pk=checkout_id)
            order = checkout.order
            site_info = SiteSetupModel.objects.first()
            
            # send mail to client and supplier
            context = {
                'domain': get_current_site(request),
                'site_info': site_info,
                'checkout': checkout,
            }
            mail_subject = '{} Order Placement'.format(SiteSetupModel.objects.first().name)
            from_email = settings.EMAIL_HOST_USER
            html_message = render_to_string('home/mail/admin_order.html', context)
            plain_message = strip_tags(html_message)
            to_mail = [site_info.email]
            if checkout.email:
                to_mail.append(checkout.email)
            
            mail_sent = send_mail(mail_subject, html_message, from_email, to_mail,
                                  html_message=html_message,
                                  fail_silently=True)
            # message admin  
            sms = "Your Order was successfully Placed, Your Order ID is {}. Thank you for choosing {}".format(str(random.randint(100, 999)) + str(checkout.id) + str(random.randint(100, 999)), site_info.name.title())
            message = """An Order was placed successfully"""
            message += """Full Name: {}""".format(checkout.full_name)
            message += """Mobile: {}""".format(checkout.mobile)
            message += """Address: {}""".format(checkout.address)
            message += """ """
            
            for index, item in enumerate(order.products.all()):
                if item.size:
                    size = '(' + item.size.size + ')'
                else:
                    size = ''
                message += """{} {} ({}) N{}""".format(item.product.name, size, order.quantity[index], order.price[index])
            message += """Transportation: {}""".format(checkout.transportation)
            message += """Total: {}""".format(checkout.grand_total)
            message += """Time of Delivery: {} {}""".format(checkout.delivery_date, checkout.delivery_time)
            
            reciever = [checkout.mobile, site_info.mobile_1]
            sender = site_info.name.upper()
            
            send_sms(sender, reciever, message)
            
            return redirect(reverse('check_out_done'))
    else:
        status = False
        amount = None

    context = {
        'payment_successful': status,
        'amount': amount,
    }
    return render(request, 'home/pay_paystack_done.html', context)


@csrf_exempt
# @require_POST
def paystack_webhook(request):
    client_ip = u'{}'.format(request.META['REMOTE_ADDR'])
    white_list = ['52.31.139.75', '52.49.173.169', '52.214.14.220', '127.0.0.1']
    if client_ip not in white_list:
        raise PermissionDenied

    authorization_key = settings.PAY_STACK_PRIVATE_KEY
    webhook_data = request.body
    hash = hmac.new(authorization_key, webhook_data, digestmod=hashlib.sha512).hexdigest()
    if hash != request.headers['HTTP_X_PAYSTACK_SIGNATURE']:
        raise ValidationError('MAC Authentication Failed')

    response_data = json.loads(request.body)
    if response_data.event == 'charge.success':
        email = response_data.data.email
        amount = response_data.amount/100
        reference = response_data.data.reference

        transaction = Transaction(authorization_key=settings.PAY_STACK_PRIVATE_KEY)
        response = transaction.verify(reference)
        status = response.status

        if status == 'success':
            user = get_object_or_404(User, email=email)
            user_wallet = get_object_or_404(UserWallet, user=user)

            user_wallet.balance += amount
            user_wallet.save()

            return HttpResponse(status=200)

