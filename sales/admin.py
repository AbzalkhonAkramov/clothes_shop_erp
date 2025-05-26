from django.contrib import admin
from .models import Category, Product, Sale

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'category', 'price')
    list_filter = ('category',)
    search_fields = ('name', 'code')

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'price', 'date', 'total')
    list_filter = ('date', 'product__category')
    date_hierarchy = 'date'
    search_fields = ('product__name',)
