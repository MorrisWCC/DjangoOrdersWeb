from django.db import models

# Create your models here.

class Product(models.Model):
    product_id = models.CharField(max_length=50, primary_key=True)
    stock_pcs = models.IntegerField(default=0)
    price = models.IntegerField(blank=False)
    shop_id = models.CharField(max_length=255, blank=False)
    vip = models.BooleanField(default=False)
    
    @staticmethod
    def get_attr():
        return ['product_id', 'stock_pcs', 'price', 'shop_id', 'vip']

class Order(models.Model):
    order_id = models.CharField(max_length=50, primary_key=True)
    product_id = models.CharField(max_length=50, blank=False)
    qty = models.IntegerField(blank=False)
    price = models.IntegerField(blank=False)
    shop_id = models.CharField(max_length=255, blank=False)

    @staticmethod
    def get_attr():
        return ['order_id', 'product_id', 'qty', 'price', 'shop_id']


