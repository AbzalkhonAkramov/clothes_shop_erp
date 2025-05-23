from django import forms
from .models import Inventory, SupplyHistory, Location

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['product', 'quantity', 'location']

class SupplyHistoryForm(forms.ModelForm):
    class Meta:
        model = SupplyHistory
        fields = ['product', 'quantity', 'date', 'supplier']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
