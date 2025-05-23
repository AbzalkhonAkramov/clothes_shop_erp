from django.contrib import admin
from .models import Department, Position, Employee

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('title', 'department')
    list_filter = ('department',)
    search_fields = ('title',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'position', 'department', 'start_date', 'salary')
    list_filter = ('department', 'position')
    search_fields = ('full_name', 'email')
    date_hierarchy = 'start_date'
