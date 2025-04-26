# Marketplace Bot

A Django-based application for automating the posting of products to Facebook Marketplace.

## Features

- **Bulk Product Upload**: Upload product details using Excel spreadsheets
- **Image Management**: Upload images individually or in bulk for each product
- **Facebook Marketplace Automation**: Automatically post products to Facebook Marketplace
- **User Authentication**: Secure login and user management

## Technologies Used

- Django
- Selenium for web automation
- Bootstrap for the frontend
- SQLite database

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/motu89/MBM12.git
   cd MBM12
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```
   python manage.py migrate
   ```

5. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

## Usage

1. Upload product details using an Excel file format
2. Upload images for each product
3. Add your Facebook credentials
4. Click on "Publish Ads On Market Place" to start posting

## License

This project is proprietary.

## Author

MOTU 