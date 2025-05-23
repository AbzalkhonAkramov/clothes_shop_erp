from django.db import models


class DashboardSetting(models.Model):
    welcome_message = models.CharField(max_length=255, default="Welcome!")
    show_sales_summary = models.BooleanField(default=True)
    show_hr_summary = models.BooleanField(default=True)
    show_warehouse_summary = models.BooleanField(default=True)

    def __str__(self):
        return "Dashboard Settings"
