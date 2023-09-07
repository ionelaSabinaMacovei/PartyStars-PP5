from django.db import models
import random
import string
from django.utils import timezone
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User
from profiles.models import UserProfile


class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'
        
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


def generate_sku():
    """Generate a random 6-digit SKU"""
    digits = string.digits
    sku = "".join(random.choice(digits) for x in range(6))

    while Product.objects.filter(sku=sku).exists():
        sku = "".join(random.choice(digits) for x in range(6))

    return sku


class Product(models.Model):
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(
        max_length=6,
        unique=True,
        default=generate_sku,
        help_text="SKU randomly generated",
    )
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    review_count = models.DecimalField(
        max_digits=6, decimal_places=0, null=True, blank=True, default=0
    )
    #on_sale = models.BooleanField(default=False)
    #sale_price = models.DecimalField(max_digits=4, decimal_places=2)
    #discount = models.IntegerField(
    #    default=10,
    #    help_text="Discount in Percentage",
     #   verbose_name="Discount If Product On Sale",
    #)
    #discounted_price = models.IntegerField(null=True)

    def clean(self):
        if self.price < 0:
            raise ValidationError("Price cannot be negative.")

    #@property
    #def discounted_price(self):
    #    return ((self.price) * (self.discount)) / 100

    #@property
    #def sale_price(self):
    #    return (self.price) - (self.discounted_price)

    def __str__(self):
        return self.name


class Review(models.Model):
    """Model for product reviews"""

    RATING = [
        (5, '5'),
        (4, '4'),
        (3, '3'),
        (2, '2'),
        (1, '1'),
    ]

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING, default=3)
    body = models.TextField(max_length=1024)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'User: {self.user} rated {self.product}, {self.product} stars.'