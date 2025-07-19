🛍️ E-Commerce API with Django REST Framework
https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray
https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white
https://img.shields.io/badge/redis-%2523DD0031.svg?style=for-the-badge&logo=redis&logoColor=white
https://img.shields.io/badge/Django%2520Channels-2.0-green?style=for-the-badge

A full-featured e-commerce API built with Django REST Framework featuring:

JWT Authentication

Product & Category Management

Order Processing System

Real-time Notifications

Redis Caching

Comprehensive Testing

📋 Table of Contents
Features

Tech Stack

Setup

Prerequisites

Installation

Environment Variables

Database Setup

Running the Server

API Documentation

Authentication

Products

Orders

WebSockets

Testing

Deployment

Troubleshooting

Contributing

License

✨ Features
User System
✅ JWT Authentication (Access & Refresh tokens)

✅ User Registration & Profile Management

✅ Secure Password Handling

✅ Order History Tracking

Product Management
✅ Product CRUD Operations (Admin Only)

✅ Category Management

✅ Stock Tracking & Updates

✅ Product Filtering & Pagination

Order System
✅ Shopping Cart Functionality

✅ Order Processing (Pending → Shipped → Delivered)

✅ Real-time Status Updates via WebSockets

✅ Order History for Users

Performance
✅ Redis Caching for Products & Categories

✅ Automatic Cache Invalidation

✅ Optimized Database Queries

🛠 Tech Stack
Backend:

Python 3.12

Django 5.2

Django REST Framework

SimpleJWT for Authentication

PostgreSQL Database

Redis for Caching & Channels Layer

Django Channels for WebSockets

Testing:

pytest

pytest-django

pytest-cov

Factory Boy

🚀 Setup
Prerequisites
Python 3.12+

PostgreSQL

Redis

Virtual Environment (recommended)

Installation
Clone the repository:

bash
git clone https://github.com/yourusername/ecommerce-api.git
cd ecommerce-api
Create and activate virtual environment:

bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
Install dependencies:

bash
pip install -r requirements.txt
Environment Variables
Create a .env file in the project root:

ini
DEBUG=True
SECRET_KEY=your-secret-key-here
DB_NAME=ecommerce
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
REDIS_URL=redis://localhost:6379/1
Database Setup
Create PostgreSQL database:

sql
CREATE DATABASE ecommerce;
CREATE USER ecommerce_user WITH PASSWORD 'ecommerce_pass';
ALTER ROLE ecommerce_user SET client_encoding TO 'utf8';
ALTER ROLE ecommerce_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE ecommerce_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE ecommerce TO ecommerce_user;
Run migrations:

bash
python manage.py migrate
Create superuser:

bash
python manage.py createsuperuser
Running the Server
Start Redis server (in separate terminal):

bash
redis-server
Run Django development server:

bash
python manage.py runserver
For WebSockets, run Daphne:

bash
daphne ecommerce_api.asgi:application
📚 API Documentation
Authentication
Base URL: /api/auth/

Endpoint	Method	Description	Auth Required
/register/	POST	Register new user	No
/login/	POST	Get JWT tokens	No
/login/refresh/	POST	Refresh access token	No
/profile/	GET/PUT	View/update user profile	Yes
Products
Base URL: /api/products/

Endpoint	Method	Description	Auth Required
/	GET	List all products (paginated)	No
/	POST	Create new product	Admin
/{id}/	GET	Get product details	No
/{id}/	PUT	Update product	Admin
/{id}/	DELETE	Delete product	Admin
Filters:

?category={id}

?min_price={value}

?max_price={value}

?in_stock=true

Orders
Base URL: /api/

Endpoint	Method	Description	Auth Required
/cart/	GET	View cart contents	Yes
/cart/items/	POST	Add item to cart	Yes
/cart/items/	DELETE	Remove item from cart	Yes
/orders/	GET	List user's orders	Yes
/orders/	POST	Create new order from cart	Yes
/orders/{id}/	GET	Get order details	Yes
/orders/{id}/status/	PATCH	Update order status (Admin)	Admin
WebSockets
Endpoint: ws://localhost:8000/ws/notifications/

Connect with valid JWT token

Receive real-time order status updates

Messages format:

json
{
  "type": "order_update",
  "order_id": 123,
  "status": "shipped",
  "message": "Your order has been shipped"
}
🧪 Testing
Run all tests with coverage:

bash
pytest --cov --cov-report=html
Key test files:

core/tests/ - Authentication & user tests

products/tests/ - Product model & view tests

orders/tests/ - Cart, orders & WebSocket tests

View coverage report:

bash
open htmlcov/index.html  # macOS
start htmlcov/index.html  # Windows
🚀 Deployment
Production Settings
Update .env:

ini
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
Recommended stack:

Gunicorn/UVicorn + Nginx

PostgreSQL

Redis

Daphne for WebSockets

Sample Nginx config:

nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /ws/ {
        proxy_pass http://127.0.0.1:8001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
🛠 Troubleshooting
Redis Connection Issues:

Ensure Redis server is running

Check Redis version (requires 5.0+)

Verify Redis URL in settings

Database Errors:

Check PostgreSQL service is running

Verify database credentials in .env

Run python manage.py migrate if schema changes

WebSocket Problems:

Ensure Daphne is running

Check Redis is configured for channels

Verify Nginx/Apache WebSocket proxying

🤝 Contributing
Fork the project

Create your feature branch (git checkout -b feature/AmazingFeature)

Commit your changes (git commit -m 'Add some AmazingFeature')

Push to the branch (git push origin feature/AmazingFeature)

Open a Pull Request

📜 License
Distributed under the MIT License. See LICENSE for more information.

This README provides comprehensive documentation for setting up, using, and maintaining the e-commerce API. The markdown formatting ensures good readability on GitHub and other platforms. Let me know if you'd like me to add or modify any sections!


