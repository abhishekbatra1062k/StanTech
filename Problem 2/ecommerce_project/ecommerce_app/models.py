from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass  # Custom User model if needed, otherwise use default

class Product(models.Model):
    product_id = models.CharField(max_length=50, unique=True)
    product_name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    price = models.FloatField()
    quantity_sold = models.IntegerField()
    rating = models.FloatField(null=True, blank=True)
    review_count = models.IntegerField()

    def __str__(self):
        return self.product_name
