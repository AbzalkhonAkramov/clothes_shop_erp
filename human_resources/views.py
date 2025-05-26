from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Employee, Department, Position
from .forms import EmployeeForm


@login_required
def employee_list(request):
    employees = Employee.objects.all().order_by('full_name')
    context = {
        'title': 'Employees',
        'employees': employees,
    }
    return render(request, 'human_resources/employee_list.html', context)


@login_required
def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm()

    context = {
        'title': 'Add Employee',
        'form': form,
    }
    return render(request, 'human_resources/add_employee.html', context)


@login_required
def department_list(request):
    departments = Department.objects.all().order_by('name')
    context = {
        'title': 'Departments',
        'departments': departments,
    }
    return render(request, 'human_resources/department_list.html', context)
