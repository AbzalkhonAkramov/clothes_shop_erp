import { execSync } from 'child_process';
import fs from 'fs';

// Create Django project structure
console.log("Setting up Django project structure...");

// Create project directory
if (!fs.existsSync('./clothes_shop_erp')) {
  fs.mkdirSync('./clothes_shop_erp');
}

// Create requirements.txt
const requirements = `
Django==4.2.7
django-crispy-forms==2.0
crispy-bootstrap4==2022.1
Pillow==10.0.0
django-filter==23.2
django-tables2==2.5.3
django-chartjs==2.3.0
`;

fs.writeFileSync('./clothes_shop_erp/requirements.txt', requirements);

// Create README.md with installation instructions
const readme = `
# Clothes Shop ERP

A Django-based ERP system for clothes shops with modules for Sales, Finance, Human Resources, and Warehouse management.

## Installation

1. Clone this repository
2. Create a virtual environment: \`python -m venv venv\`
3. Activate the virtual environment:
   - Windows: \`venv\\Scripts\\activate\`
   - Linux/Mac: \`source venv/bin/activate\`
4. Install dependencies: \`pip install -r requirements.txt\`
5. Run migrations: \`python manage.py migrate\`
6. Create a superuser: \`python manage.py createsuperuser\`
7. Load demo data: \`python manage.py loaddata demo_data.json\`
8. Run the server: \`python manage.py runserver\`
9. Access the admin panel at http://127.0.0.1:8000/admin/
10. Access the ERP system at http://127.0.0.1:8000/

## Features

- Dashboard with key metrics and charts
- Sales management and reporting
- Human Resources management
- Warehouse and inventory management
- Finance tracking
`;

fs.writeFileSync('./clothes_shop_erp/README.md', readme);

console.log("Project structure set up successfully!");
console.log("Next steps:");
console.log("1. Create Django project and apps");
console.log("2. Set up models for each module");
console.log("3. Create views and templates");
console.log("4. Add static files (CSS, JS, images)");
console.log("5. Configure URLs and settings");