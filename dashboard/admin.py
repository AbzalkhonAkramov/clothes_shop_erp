from django.contrib import admin
from .models import DashboardSetting

@admin.register(DashboardSetting)
class DashboardSettingAdmin(admin.ModelAdmin):
    list_display = ('welcome_message', 'show_sales_summary', 'show_hr_summary', 'show_warehouse_summary')
