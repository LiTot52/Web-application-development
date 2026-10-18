from django.db import models

# Create your models here.
# pip install
# Pillow


class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    created_ad = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/')


class Order(models.Model):
    customer_name = models.CharField(max_length=200)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    delivery_address = models.TextField(blank=True)


def __str__(self):
    return self.title
