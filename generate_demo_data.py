import os
import django
import random
from datetime import datetime, timedelta

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clothes_shop_erp.settings')
django.setup()

from django.contrib.auth.models import User
from sales.models import Category, Product, Sale
from human_resources.models import Department, Position, Employee
from warehouse.models import Location, Inventory, SupplyHistory
from finance.models import Transaction

# Create superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created')

# Create categories
categories = [
    {'name': 'T-Shirts', 'description': 'Casual and comfortable t-shirts'},
    {'name': 'Jeans', 'description': 'Denim jeans for all occasions'},
    {'name': 'Dresses', 'description': 'Elegant dresses for women'},
    {'name': 'Shirts', 'description': 'Formal and casual shirts for men'},
    {'name': 'Jackets', 'description': 'Stylish jackets for all seasons'},
    {'name': 'Accessories', 'description': 'Belts, hats, and other accessories'},
]

for category_data in categories:
    Category.objects.get_or_create(
        name=category_data['name'],
        defaults={'description': category_data['description']}
    )
    print(f"Category created: {category_data['name']}")

# Create products
products = [
    {'name': 'Basic T-Shirt', 'code': 'TS-001', 'category': 'T-Shirts', 'price': 29.99},
    {'name': 'Graphic T-Shirt', 'code': 'TS-002', 'category': 'T-Shirts', 'price': 39.99},
    {'name': 'V-Neck T-Shirt', 'code': 'TS-003', 'category': 'T-Shirts', 'price': 34.99},
    {'name': 'Slim Fit Jeans', 'code': 'JN-001', 'category': 'Jeans', 'price': 59.99},
    {'name': 'Bootcut Jeans', 'code': 'JN-002', 'category': 'Jeans', 'price': 64.99},
    {'name': 'Skinny Jeans', 'code': 'JN-003', 'category': 'Jeans', 'price': 69.99},
    {'name': 'Summer Dress', 'code': 'DR-001', 'category': 'Dresses', 'price': 79.99},
    {'name': 'Evening Dress', 'code': 'DR-002', 'category': 'Dresses', 'price': 129.99},
    {'name': 'Casual Dress', 'code': 'DR-003', 'category': 'Dresses', 'price': 89.99},
    {'name': 'Formal Shirt', 'code': 'SH-001', 'category': 'Shirts', 'price': 49.99},
    {'name': 'Casual Shirt', 'code': 'SH-002', 'category': 'Shirts', 'price': 44.99},
    {'name': 'Denim Shirt', 'code': 'SH-003', 'category': 'Shirts', 'price': 54.99},
    {'name': 'Leather Jacket', 'code': 'JK-001', 'category': 'Jackets', 'price': 149.99},
    {'name': 'Denim Jacket', 'code': 'JK-002', 'category': 'Jackets', 'price': 99.99},
    {'name': 'Bomber Jacket', 'code': 'JK-003', 'category': 'Jackets', 'price': 119.99},
    {'name': 'Leather Belt', 'code': 'AC-001', 'category': 'Accessories', 'price': 29.99},
    {'name': 'Fedora Hat', 'code': 'AC-002', 'category': 'Accessories', 'price': 34.99},
    {'name': 'Silk Scarf', 'code': 'AC-003', 'category': 'Accessories', 'price': 24.99},
]

for product_data in products:
    category = Category.objects.get(name=product_data['category'])
    Product.objects.get_or_create(
        code=product_data['code'],
        defaults={
            'name': product_data['name'],
            'category': category,
            'price': product_data['price'],
            'description': f"Description for {product_data['name']}"
        }
    )
    print(f"Product created: {product_data['name']}")

# Create departments
departments = [
    {'name': 'Sales', 'description': 'Sales and marketing department'},
    {'name': 'Finance', 'description': 'Financial management department'},
    {'name': 'Human Resources', 'description': 'HR department'},
    {'name': 'Warehouse', 'description': 'Inventory and logistics department'},
    {'name': 'Customer Service', 'description': 'Customer support department'},
]

for department_data in departments:
    Department.objects.get_or_create(
        name=department_data['name'],
        defaults={'description': department_data['description']}
    )
    print(f"Department created: {department_data['name']}")

# Create positions
positions = [
    {'title': 'Sales Manager', 'department': 'Sales'},
    {'title': 'Sales Associate', 'department': 'Sales'},
    {'title': 'Marketing Specialist', 'department': 'Sales'},
    {'title': 'Financial Analyst', 'department': 'Finance'},
    {'title': 'Accountant', 'department': 'Finance'},
    {'title': 'HR Manager', 'department': 'Human Resources'},
    {'title': 'HR Specialist', 'department': 'Human Resources'},
    {'title': 'Warehouse Manager', 'department': 'Warehouse'},
    {'title': 'Inventory Specialist', 'department': 'Warehouse'},
    {'title': 'Customer Service Representative', 'department': 'Customer Service'},
    {'title': 'Customer Service Manager', 'department': 'Customer Service'},
]

for position_data in positions:
    department = Department.objects.get(name=position_data['department'])
    Position.objects.get_or_create(
        title=position_data['title'],
        department=department,
        defaults={'description': f"Description for {position_data['title']}"}
    )
    print(f"Position created: {position_data['title']}")

# Create employees
employees = [
    {'full_name': 'John Smith', 'position': 'Sales Manager', 'department': 'Sales', 'salary': 5000},
    {'full_name': 'Jane Doe', 'position': 'Sales Associate', 'department': 'Sales', 'salary': 3000},
    {'full_name': 'Michael Johnson', 'position': 'Marketing Specialist', 'department': 'Sales', 'salary': 3500},
    {'full_name': 'Emily Davis', 'position': 'Financial Analyst', 'department': 'Finance', 'salary': 4500},
    {'full_name': 'Robert Wilson', 'position': 'Accountant', 'department': 'Finance', 'salary': 4000},
    {'full_name': 'Sarah Brown', 'position': 'HR Manager', 'department': 'Human Resources', 'salary': 5000},
    {'full_name': 'David Miller', 'position': 'HR Specialist', 'department': 'Human Resources', 'salary': 3500},
    {'full_name': 'Jennifer Taylor', 'position': 'Warehouse Manager', 'department': 'Warehouse', 'salary': 4500},
    {'full_name': 'William Anderson', 'position': 'Inventory Specialist', 'department': 'Warehouse', 'salary': 3000},
    {'full_name': 'Lisa Thomas', 'position': 'Customer Service Representative', 'department': 'Customer Service',
     'salary': 2800},
    {'full_name': 'James Jackson', 'position': 'Customer Service Manager', 'department': 'Customer Service',
     'salary': 4200},
]

for employee_data in employees:
    department = Department.objects.get(name=employee_data['department'])
    position = Position.objects.get(title=employee_data['position'], department=department)

    # Generate a random start date within the last 3 years
    start_date = datetime.now().date() - timedelta(days=random.randint(30, 1095))

    Employee.objects.get_or_create(
        full_name=employee_data['full_name'],
        defaults={
            'position': position,
            'department': department,
            'start_date': start_date,
            'salary': employee_data['salary'],
            'email': f"{employee_data['full_name'].lower().replace(' ', '.')}@example.com",
            'phone': f"+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
        }
    )
    print(f"Employee created: {employee_data['full_name']}")

# Create locations
locations = [
    {'name': 'Main Warehouse', 'description': 'Main storage facility'},
    {'name': 'Store Backroom', 'description': 'Storage at the retail store'},
    {'name': 'Outlet Storage', 'description': 'Storage at the outlet store'},
]

for location_data in locations:
    Location.objects.get_or_create(
        name=location_data['name'],
        defaults={'description': location_data['description']}
    )
    print(f"Location created: {location_data['name']}")

# Create inventory and supply history
main_location = Location.objects.get(name='Main Warehouse')
today = datetime.now().date()

for product in Product.objects.all():
    # Create inventory
    quantity = random.randint(10, 100)
    inventory, created = Inventory.objects.get_or_create(
        product=product,
        defaults={
            'quantity': quantity,
            'location': main_location
        }
    )

    if created:
        print(f"Inventory created for: {product.name}")

    # Create supply history (last 6 months)
    for i in range(3):
        supply_date = today - timedelta(days=random.randint(1, 180))
        supply_quantity = random.randint(5, 50)

        SupplyHistory.objects.create(
            product=product,
            quantity=supply_quantity,
            date=supply_date,
            supplier=random.choice(['Supplier A', 'Supplier B', 'Supplier C'])
        )

    print(f"Supply history created for: {product.name}")

# Create sales (last 6 months)
for i in range(100):
    product = random.choice(list(Product.objects.all()))
    quantity = random.randint(1, 5)
    sale_date = today - timedelta(days=random.randint(1, 180))

    Sale.objects.create(
        product=product,
        quantity=quantity,
        price=product.price,
        date=sale_date
    )

print(f"Created 100 sales records")

# Create financial transactions (last 6 months)
transaction_categories = ['Sales', 'Rent', 'Utilities', 'Salaries', 'Supplies', 'Marketing', 'Maintenance']

for i in range(50):
    transaction_type = random.choice(['income', 'expense'])
    amount = random.uniform(100, 5000)
    transaction_date = today - timedelta(days=random.randint(1, 180))
    category = random.choice(transaction_categories)

    Transaction.objects.create(
        description=f"{category} {'revenue' if transaction_type == 'income' else 'payment'}",
        amount=amount,
        transaction_type=transaction_type,
        date=transaction_date,
        category=category
    )

print(f"Created 50 financial transactions")

print("Demo data generation complete!")