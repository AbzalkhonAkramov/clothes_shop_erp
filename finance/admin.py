from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('description', 'amount', 'transaction_type', 'date', 'category')
    list_filter = ('transaction_type', 'date', 'category')
    date_hierarchy = 'date'
    search_fields = ('description', 'category')
