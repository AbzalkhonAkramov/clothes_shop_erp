from django.contrib import admin
from .models import Location, Inventory, SupplyHistory

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'location', 'last_updated')
    list_filter = ('location', 'product__category')
    search_fields = ('product__name',)

@admin.register(SupplyHistory)
class SupplyHistoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'date', 'supplier')
    list_filter = ('date', 'product__category')
    date_hierarchy = 'date'
    search_fields = ('product__name', 'supplier')
