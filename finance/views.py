from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Transaction
from .forms import TransactionForm
import json


@login_required
def finance_dashboard(request):
    # Get current date and date ranges
    today = timezone.now().date()
    start_of_month = today.replace(day=1)
    start_of_prev_month = (start_of_month - timedelta(days=1)).replace(day=1)
    start_of_year = today.replace(month=1, day=1)

    # Get monthly income and expenses
    monthly_income = Transaction.objects.filter(
        transaction_type='income',
        date__gte=start_of_month
    ).aggregate(total=Sum('amount'))['total'] or 0

    monthly_expenses = Transaction.objects.filter(
        transaction_type='expense',
        date__gte=start_of_month
    ).aggregate(total=Sum('amount'))['total'] or 0

    # Get yearly income and expenses
    yearly_income = Transaction.objects.filter(
        transaction_type='income',
        date__gte=start_of_year
    ).aggregate(total=Sum('amount'))['total'] or 0

    yearly_expenses = Transaction.objects.filter(
        transaction_type='expense',
        date__gte=start_of_year
    ).aggregate(total=Sum('amount'))['total'] or 0

    # Calculate net profit
    monthly_profit = monthly_income - monthly_expenses
    yearly_profit = yearly_income - yearly_expenses

    # Calculate month-over-month growth
    prev_month_income = Transaction.objects.filter(
        transaction_type='income',
        date__gte=start_of_prev_month,
        date__lt=start_of_month
    ).aggregate(total=Sum('amount'))['total'] or 0

    if prev_month_income > 0:
        mom_growth = ((monthly_income - prev_month_income) / prev_month_income) * 100
    else:
        mom_growth = 0

    # Get recent transactions
    recent_transactions = Transaction.objects.all().order_by('-date')[:10]

    # Get transactions by category
    expense_by_category = Transaction.objects.filter(
        transaction_type='expense',
        date__gte=start_of_month
    ).values('category').annotate(
        total=Sum('amount')
    ).order_by('-total')

    # Prepare data for charts
    # Last 6 months of data for line chart
    months_data = []
    income_data = []
    expense_data = []

    for i in range(5, -1, -1):
        # Calculate the start and end of each month
        month_start = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
        month_start = month_start.replace(month=((month_start.month - i - 1) % 12) + 1)
        if month_start.month > today.month:
            month_start = month_start.replace(year=today.year - 1)

        if i > 0:
            month_end = (month_start.replace(month=month_start.month % 12 + 1, day=1) - timedelta(days=1))
        else:
            month_end = today

        # Get income and expenses for the month
        month_income = Transaction.objects.filter(
            transaction_type='income',
            date__gte=month_start,
            date__lte=month_end
        ).aggregate(total=Sum('amount'))['total'] or 0

        month_expense = Transaction.objects.filter(
            transaction_type='expense',
            date__gte=month_start,
            date__lte=month_end
        ).aggregate(total=Sum('amount'))['total'] or 0

        # Add to data arrays
        months_data.append(month_start.strftime('%b %Y'))
        income_data.append(float(month_income))
        expense_data.append(float(month_expense))

    # Prepare data for pie chart
    category_labels = [item['category'] or 'Uncategorized' for item in expense_by_category]
    category_data = [float(item['total']) for item in expense_by_category]

    context = {
        'title': 'Finance Dashboard',
        'monthly_income': monthly_income,
        'monthly_expenses': monthly_expenses,
        'monthly_profit': monthly_profit,
        'yearly_income': yearly_income,
        'yearly_expenses': yearly_expenses,
        'yearly_profit': yearly_profit,
        'mom_growth': mom_growth,
        'recent_transactions': recent_transactions,
        'expense_by_category': expense_by_category,
        'months_data': json.dumps(months_data),
        'income_data': json.dumps(income_data),
        'expense_data': json.dumps(expense_data),
        'category_labels': json.dumps(category_labels),
        'category_data': json.dumps(category_data),
    }

    return render(request, 'finance/dashboard.html', context)


@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('finance_dashboard')
    else:
        form = TransactionForm()

    context = {
        'title': 'Add Transaction',
        'form': form,
    }

    return render(request, 'finance/add_transaction.html', context)


@login_required
def transaction_list(request):
    transactions = Transaction.objects.all().order_by('-date')

    context = {
        'title': 'Transactions',
        'transactions': transactions,
    }

    return render(request, 'finance/transaction_list.html', context)
