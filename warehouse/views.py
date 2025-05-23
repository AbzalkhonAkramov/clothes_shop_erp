from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Inventory, SupplyHistory, Location
from .forms import InventoryForm, SupplyHistoryForm


@login_required
def inventory_list(request):
    inventory_items = Inventory.objects.all().order_by('product__name')
    context = {
        'title': 'Inventory',
        'inventory_items': inventory_items,
    }
    return render(request, 'warehouse/inventory_list.html', context)


@login_required
def add_inventory(request):
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory_list')
    else:
        form = InventoryForm()

    context = {
        'title': 'Add Inventory',
        'form': form,
    }
    return render(request, 'warehouse/add_inventory.html', context)


@login_required
def add_supply(request):
    if request.method == 'POST':
        form = SupplyHistoryForm(request.POST)
        if form.is_valid():
            supply = form.save()

            # Update inventory quantity
            inventory, created = Inventory.objects.get_or_create(
                product=supply.product,
                defaults={'quantity': 0, 'location': Location.objects.first()}
            )

            inventory.quantity += supply.quantity
            inventory.save()

            return redirect('inventory_list')
    else:
        form = SupplyHistoryForm()

    context = {
        'title': 'Add Supply',
        'form': form,
    }
    return render(request, 'warehouse/add_supply.html', context)
