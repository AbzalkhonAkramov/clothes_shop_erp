from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Avg, F, ExpressionWrapper, DecimalField
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import datetime, timedelta
import json

from sales.models import Sale, Product, Category
from human_resources.models import Employee, Department
from warehouse.models import Inventory, SupplyHistory
from finance.models import Transaction


@login_required
def dashboard(request):
    # Get current date and date ranges
    today = timezone.now().date()
    yesterday = today - timedelta(days=1)
    start_of_month = today.replace(day=1)
    start_of_prev_month = (start_of_month - timedelta(days=1)).replace(day=1)
    start_of_year = today.replace(month=1, day=1)

    # Date range for charts (last 30 days)
    date_30_days_ago = today - timedelta(days=30)

    # -----------------
    # SALES METRICS
    # -----------------

    # Total sales for current month
    monthly_sales = Sale.objects.filter(date__gte=start_of_month).aggregate(
        total_amount=Sum(F('price') * F('quantity')),
        total_quantity=Sum('quantity')
    )

    monthly_sales_amount = monthly_sales['total_amount'] or 0
    monthly_sales_quantity = monthly_sales['total_quantity'] or 0

    # Previous month sales for comparison
    prev_month_sales = Sale.objects.filter(
        date__gte=start_of_prev_month,
        date__lt=start_of_month
    ).aggregate(
        total_amount=Sum(F('price') * F('quantity'))
    )

    prev_month_sales_amount = prev_month_sales['total_amount'] or 0

    # Calculate sales growth
    if prev_month_sales_amount > 0:
        sales_growth = ((monthly_sales_amount - prev_month_sales_amount) / prev_month_sales_amount) * 100
    else:
        sales_growth = 100  # If previous month was 0, consider it 100% growth

    # Best selling products
    best_selling_products = Product.objects.annotate(
        total_sold=Sum('sales__quantity')
    ).filter(total_sold__gt=0).order_by('-total_sold')[:5]

    # Best selling categories
    best_selling_categories = Category.objects.annotate(
        total_sold=Sum('products__sales__quantity')
    ).filter(total_sold__gt=0).order_by('-total_sold')[:5]

    # Recent sales
    recent_sales = Sale.objects.select_related('product').order_by('-date')[:5]

    # Sales by month for chart
    sales_by_month = Sale.objects.annotate(
        month=TruncMonth('date')
    ).values('month').annotate(
        total=Sum(F('price') * F('quantity'))
    ).order_by('month')

    # Prepare sales chart data
    sales_chart_labels = []
    sales_chart_data = []

    for i in range(6):
        month_date = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
        month_date = month_date.replace(month=((month_date.month - i - 1) % 12) + 1)
        if month_date.month > today.month:
            month_date = month_date.replace(year=today.year - 1)

        month_name = month_date.strftime('%b %Y')
        sales_chart_labels.insert(0, month_name)

        # Find the sales for this month
        month_sales = next(
            (item['total'] for item in sales_by_month if
             item['month'].month == month_date.month and item['month'].year == month_date.year),
            0
        )

        sales_chart_data.insert(0, float(month_sales))

    # -----------------
    # FINANCE METRICS
    # -----------------

    # Monthly income and expenses
    monthly_income = Transaction.objects.filter(
        transaction_type='income',
        date__gte=start_of_month
    ).aggregate(total=Sum('amount'))['total'] or 0

    monthly_expenses = Transaction.objects.filter(
        transaction_type='expense',
        date__gte=start_of_month
    ).aggregate(total=Sum('amount'))['total'] or 0

    # Calculate profit
    monthly_profit = monthly_income - monthly_expenses

    # Expense breakdown by category
    expense_by_category = Transaction.objects.filter(
        transaction_type='expense',
        date__gte=start_of_month
    ).values('category').annotate(
        total=Sum('amount')
    ).order_by('-total')[:5]

    # Prepare expense chart data
    expense_chart_labels = [item['category'] or 'Uncategorized' for item in expense_by_category]
    expense_chart_data = [float(item['total']) for item in expense_by_category]

    # Recent transactions
    recent_transactions = Transaction.objects.order_by('-date')[:5]

    # -----------------
    # HR METRICS
    # -----------------

    # Total employees
    total_employees = Employee.objects.count()

    # Department breakdown
    departments = Department.objects.annotate(
        employee_count=Count('employees')
    ).order_by('-employee_count')

    # Prepare department chart data
    dept_chart_labels = [dept.name for dept in departments]
    dept_chart_data = [dept.employee_count for dept in departments]

    # Recent employees
    recent_employees = Employee.objects.order_by('-start_date')[:5]

    # Average salary
    avg_salary = Employee.objects.aggregate(avg=Avg('salary'))['avg'] or 0

    # -----------------
    # WAREHOUSE METRICS
    # -----------------

    # Total inventory value
    inventory_value = Inventory.objects.annotate(
        value=ExpressionWrapper(F('quantity') * F('product__price'), output_field=DecimalField())
    ).aggregate(total=Sum('value'))['total'] or 0

    # Low stock items (less than 10 units)
    low_stock_items = Inventory.objects.filter(quantity__lt=10).order_by('quantity')
    low_stock_count = low_stock_items.count()

    # Recent supplies
    recent_supplies = SupplyHistory.objects.select_related('product').order_by('-date')[:5]

    # Top inventory items by value
    top_inventory_items = Inventory.objects.annotate(
        value=ExpressionWrapper(F('quantity') * F('product__price'), output_field=DecimalField())
    ).order_by('-value')[:5]

    # Prepare inventory chart data
    inventory_chart_labels = [item.product.category.name for item in top_inventory_items]
    inventory_chart_data = [float(item.value) for item in top_inventory_items]

    context = {
        'title': 'Dashboard',

        # Sales metrics
        'monthly_sales_amount': monthly_sales_amount,
        'monthly_sales_quantity': monthly_sales_quantity,
        'sales_growth': sales_growth,
        'best_selling_products': best_selling_products,
        'best_selling_categories': best_selling_categories,
        'recent_sales': recent_sales,
        'sales_chart_labels': json.dumps(sales_chart_labels),
        'sales_chart_data': json.dumps(sales_chart_data),

        # Finance metrics
        'monthly_income': monthly_income,
        'monthly_expenses': monthly_expenses,
        'monthly_profit': monthly_profit,
        'expense_by_category': expense_by_category,
        'expense_chart_labels': json.dumps(expense_chart_labels),
        'expense_chart_data': json.dumps(expense_chart_data),
        'recent_transactions': recent_transactions,

        # HR metrics
        'total_employees': total_employees,
        'departments': departments,
        'dept_chart_labels': json.dumps(dept_chart_labels),
        'dept_chart_data': json.dumps(dept_chart_data),
        'recent_employees': recent_employees,
        'avg_salary': avg_salary,

        # Warehouse metrics
        'inventory_value': inventory_value,
        'low_stock_count': low_stock_count,
        'low_stock_items': low_stock_items,
        'recent_supplies': recent_supplies,
        'inventory_chart_labels': json.dumps(inventory_chart_labels),
        'inventory_chart_data': json.dumps(inventory_chart_data),
    }

    return render(request, 'dashboard/dashboard.html', context)
