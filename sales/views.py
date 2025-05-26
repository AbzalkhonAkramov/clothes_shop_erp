from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Sale, Product, Category
from .forms import SaleForm, ProductForm


@login_required
def sales_dashboard(request):
    context = {
        'title': 'Sales Dashboard',
    }
    return render(request, 'sales/dashboard.html', context)


@login_required
def product_list(request):
    products = Product.objects.all().order_by('name')
    context = {
        'title': 'Products',
        'products': products,
    }
    return render(request, 'sales/product_list.html', context)


@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()

    context = {
        'title': 'Add Product',
        'form': form,
    }
    return render(request, 'sales/add_product.html', context)


@login_required
def add_sale(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sales_dashboard')
    else:
        form = SaleForm()

    context = {
        'title': 'Add Sale',
        'form': form,
    }
    return render(request, 'sales/add_sale.html', context)
