
# Clothes Shop ERP

A Django-based ERP system for clothes shops with modules for Sales, Finance, Human Resources, and Warehouse management.

## Installation

1. Clone this repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run migrations: `python manage.py migrate`
6. Create a superuser: `python manage.py createsuperuser`
7. Load demo data: `python manage.py loaddata demo_data.json`
8. Run the server: `python manage.py runserver`
9. Access the admin panel at http://127.0.0.1:8000/admin/
10. Access the ERP system at http://127.0.0.1:8000/

## Features

- Dashboard with key metrics and charts
- Sales management and reporting
- Human Resources management
- Warehouse and inventory management
- Finance tracking
