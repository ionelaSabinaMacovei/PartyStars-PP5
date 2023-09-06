from django.db import models


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
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    on_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(max_digits=4, decimal_places=2)
    discount = models.IntegerField(
        default=10,
        help_text="Discount in Percentage",
        verbose_name="Discount If Product On Sale",
    )
    discounted_price = models.IntegerField(null=True)

    def clean(self):
        if self.price < 0:
            raise ValidationError("Price cannot be negative.")

    @property
    def discounted_price(self):
        return ((self.price) * (self.discount)) / 100

    @property
    def sale_price(self):
        return (self.price) - (self.discounted_price)

    def __str__(self):
        return self.name


class Reviews(models.Model):
    """Model for product reviews"""

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=1500, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "product"], name="reviews_per_user")
        ]

    def __str__(self):
        return self.title