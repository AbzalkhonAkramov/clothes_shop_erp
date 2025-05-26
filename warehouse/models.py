from django.db import models
from sales.models import Product


class Location(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Inventory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='inventory')
    quantity = models.PositiveIntegerField(default=0)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='inventories')
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} units"

    class Meta:
        verbose_name_plural = "Inventories"


class SupplyHistory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='supply_history')
    quantity = models.PositiveIntegerField()
    date = models.DateField()
    supplier = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} units on {self.date}"

    class Meta:
        verbose_name_plural = "Supply Histories"
