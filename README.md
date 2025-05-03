# Facebook Marketplace Bot

A Django web application for automating Facebook Marketplace listings.

## Features

- Automated posting of products to Facebook Marketplace
- Multi-account support for Facebook credentials
- Product management with Excel import
- User authentication and profile management
- Image upload and management

## Technology Stack

- Django 3.2
- Selenium for web automation
- Pandas for data processing
- Bootstrap for frontend
- SQLite for database (configurable for other databases)

## Setup Instructions

### Prerequisites

- Python 3.7+
- Chrome browser
- ChromeDriver (included in the repository)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/motu89/marketplacebot.git
cd marketplacebot
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Linux/Mac
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

7. Access the application at http://127.0.0.1:8000

## Usage

1. Log in with your credentials
2. Set up your Facebook account credentials in the dashboard
3. Import products using Excel template
4. Upload images for your products
5. Click "Publish" to post your products to Facebook Marketplace

## License

This project is licensed under the MIT License - see the LICENSE file for details. 