from django.contrib import admin
from order.models import OrderModel, CheckOutModel


admin.site.register(OrderModel)
admin.site.register(CheckOutModel)
