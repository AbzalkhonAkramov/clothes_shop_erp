from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['description', 'amount', 'transaction_type', 'date', 'category']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.TextInput(attrs={'placeholder': 'Enter description'}),
            'category': forms.TextInput(attrs={'placeholder': 'Enter category (optional)'}),
        }
