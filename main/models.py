from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('boys_fashion', 'Boys Fashion'),
        ('girls_fashion', 'Girls Fashion'),
        ('soap', 'Soap'),
        ('stroller', 'Stroller'),
        ('bottle', 'Bottle'),
        ('offers', 'Offers'),
        ('pampers', 'Pampers'),
    ]
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
from django.db import models

# Create your models here.
