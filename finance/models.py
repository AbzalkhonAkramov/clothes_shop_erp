from django.db import models
from django.utils import timezone


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )

    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    date = models.DateField(default=timezone.now)
    category = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.description} - {self.amount} ({self.get_transaction_type_display()})"
