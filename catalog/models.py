from django.db import models
from django.db.models import Sum
import random


class CategoryModel(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.FileField(upload_to='images/category')

    def __str__(self):
        return self.title.upper()

    def no_of_product(self):
        return ProductModel.objects.filter(category=self).count()


class ProductModel(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE)
    description = models.TextField()
    image = models.FileField(upload_to='images/product')
    keys = models.CharField(max_length=200, null=True, blank=True)

    def save(self, *args, **kwargs):
        keys = "{} {} {}".format(self.name, self.category.title, self.description)
        self.keys = keys
        super(ProductModel, self).save(*args, **kwargs)
    
    def has_variant(self):
        return ProductVariantModel.objects.filter(product=self).count()
        
    def has_many_variant(self):
        variants = ProductVariantModel.objects.filter(product=self).count()
        if variants > 1:
            return True
        return False
        
    def start_price(self):
        return ProductVariantModel.objects.filter(product=self).order_by('price').first().price
        
    def end_price(self):
        return ProductVariantModel.objects.filter(product=self).order_by('price').last().price
        
    def first_variant(self):
        return ProductVariantModel.objects.filter(product=self).order_by('price').first()
        
    def all_variants(self):
        return ProductVariantModel.objects.filter(product=self)


class ProductSizeModel(models.Model):
    size = models.CharField(max_length=100)

    def __str__(self):
        return self.size.upper()


class ProductVariantModel(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='variant')
    size = models.ForeignKey(ProductSizeModel, on_delete=models.CASCADE, null=True, blank=True)
    price = models.FloatField()
    main_view = models.FileField(upload_to='images/product_variant', blank=True, null=True)
    side_view = models.FileField(upload_to='images/product_variant', blank=True, null=True)
    top_view = models.FileField(upload_to='images/product_variant', blank=True, null=True)
    keys = models.CharField(max_length=200, null=True, blank=True)

    def save(self, *args, **kwargs):
        keys = "{} {} {} {}".format(self.product.name, self.product.category.title, self.size, self.product.description)
        self.keys = keys
        super(ProductVariantModel, self).save(*args, **kwargs)

    def related_products(self):
        return sorted(ProductModel.objects.filter(category=self.product.category).exclude(pk=self.product.id),
                      key=lambda x: random.random())[:4]
                      
    def other_sizes(self):
        return ProductVariantModel.objects.filter(product=self.product)
