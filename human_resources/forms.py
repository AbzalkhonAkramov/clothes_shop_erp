from django import forms
from .models import Employee, Department, Position

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['title', 'department', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['full_name', 'position', 'department', 'start_date', 'salary', 'photo', 'email', 'phone']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
        }
