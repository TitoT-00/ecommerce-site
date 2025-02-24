# E-commerce Website

A remade e-commerce website built with Flask and Stripe integration.

This was a personal project back in the e'old days and it is remade now for anyone to use and learning purposes.

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory and add your configuration:
```
FLASK_APP=app.py
FLASK_ENV=development
STRIPE_SECRET_KEY=your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key
DATABASE_URL=your_database_url
```

4. Run the application:
```bash
flask run
```

## Features
- Product catalog with categories
- Shopping cart functionality
- User authentication
- Stripe payment integration
- Database integration ready
- Responsive design
