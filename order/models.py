from django.db import models
from catalog.models import ProductVariantModel


class OrderModel(models.Model):
    code = models.CharField(max_length=50, null=True)
    products = models.ManyToManyField(ProductVariantModel)
    quantity = models.JSONField(null=True)
    price = models.JSONField(null=True)
    amount = models.FloatField()
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    has_paid = models.BooleanField()
    status = models.CharField(max_length=20)


class CheckOutModel(models.Model):
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150)
    address = models.TextField()
    mobile = models.CharField(max_length=20)
    email = models.EmailField(null=True)
    delivery_date = models.DateField(null=True, blank=True)
    delivery_time = models.TimeField(null=True, blank=True)
    payment_method = models.CharField(max_length=20)
    transportation = models.FloatField()
    grand_total = models.FloatField()
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
