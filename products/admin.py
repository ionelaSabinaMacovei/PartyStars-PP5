from django.contrib import admin
from .models import Product, Category, Review

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'review_count',
        'image',
    )

    ordering = ('sku',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )

    search_fields = ('friendly_name', 'name',)


class ReviewAdmin(admin.ModelAdmin):
    """review model display"""
    list_display = (
        'user',
        'rating',
        'product',
        'created_on'

    )

    search_fields = ('user', 'product',)
    ordering = ('-created_on',)


admin.site.register(Review, ReviewAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
