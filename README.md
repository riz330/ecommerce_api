# 🛍️ E-Commerce API with Django REST Framework

![Django REST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)
![Django Channels](https://img.shields.io/badge/Django%20Channels-2.0-green?style=for-the-badge)

A comprehensive e-commerce API built with Django REST Framework, featuring JWT authentication, real-time notifications, order processing, and Redis caching for optimal performance.

## 📋 Table of Contents

- [✨ Features](#-features)
- [🛠 Tech Stack](#-tech-stack)
- [🚀 Quick Start](#-quick-start)
- [📚 API Documentation](#-api-documentation)
- [🧪 Testing](#-testing)
- [🚀 Deployment](#-deployment)
- [🛠 Troubleshooting](#-troubleshooting)
- [🤝 Contributing](#-contributing)
- [📜 License](#-license)

## ✨ Features

### 🔐 Authentication & User Management
- JWT Authentication with Access & Refresh tokens
- Secure user registration and profile management
- Password security and validation
- Complete order history tracking

### 📦 Product Management
- Full CRUD operations for products (Admin only)
- Hierarchical category management
- Real-time stock tracking and updates
- Advanced filtering and pagination

### 🛒 Order Processing System
- Dynamic shopping cart functionality
- Complete order lifecycle (Pending → Shipped → Delivered)
- Real-time status updates via WebSockets
- Comprehensive order history

### ⚡ Performance & Optimization
- Redis caching for products and categories
- Intelligent cache invalidation
- Optimized database queries
- Real-time notifications

## 🛠 Tech Stack

**Backend Framework:**
- Python 3.12
- Django 5.2
- Django REST Framework
- SimpleJWT for Authentication

**Database & Caching:**
- PostgreSQL
- Redis (Caching & Channels Layer)

**Real-time Features:**
- Django Channels for WebSockets

**Testing Suite:**
- pytest & pytest-django
- pytest-cov for coverage
- Factory Boy for test data

## 🚀 Quick Start

### Prerequisites

Ensure you have the following installed:
- Python 3.12+
- PostgreSQL
- Redis
- Virtual Environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ecommerce-api.git
   cd ecommerce-api
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Environment Configuration

Create a `.env` file in the project root:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DB_NAME=ecommerce
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
REDIS_URL=redis://localhost:6379/1
```

### Database Setup

1. **Create PostgreSQL database**
   ```sql
   CREATE DATABASE ecommerce;
   CREATE USER ecommerce_user WITH PASSWORD 'ecommerce_pass';
   ALTER ROLE ecommerce_user SET client_encoding TO 'utf8';
   ALTER ROLE ecommerce_user SET default_transaction_isolation TO 'read committed';
   ALTER ROLE ecommerce_user SET timezone TO 'UTC';
   GRANT ALL PRIVILEGES ON DATABASE ecommerce TO ecommerce_user;
   ```

2. **Run migrations**
   ```bash
   python manage.py migrate
   ```

3. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

### Running the Application

1. **Start Redis server** (in separate terminal)
   ```bash
   redis-server
   ```

2. **Run Django development server**
   ```bash
   python manage.py runserver
   ```

3. **For WebSocket support, run Daphne**
   ```bash
   daphne ecommerce_api.asgi:application
   ```

## 📚 API Documentation

### 🔐 Authentication Endpoints
**Base URL:** `/api/auth/`

| Endpoint | Method | Description | Auth Required |
|----------|---------|-------------|---------------|
| `/register/` | POST | Register new user | No |
| `/login/` | POST | Get JWT tokens | No |
| `/login/refresh/` | POST | Refresh access token | No |
| `/profile/` | GET/PUT | View/update user profile | Yes |

### 📦 Product Endpoints
**Base URL:** `/api/products/`

| Endpoint | Method | Description | Auth Required |
|----------|---------|-------------|---------------|
| `/` | GET | List all products (paginated) | No |
| `/` | POST | Create new product | Admin |
| `/{id}/` | GET | Get product details | No |
| `/{id}/` | PUT | Update product | Admin |
| `/{id}/` | DELETE | Delete product | Admin |

**Available Filters:**
- `?category={id}` - Filter by category
- `?min_price={value}` - Minimum price filter
- `?max_price={value}` - Maximum price filter
- `?in_stock=true` - Show only in-stock items

### 🛒 Order Management Endpoints
**Base URL:** `/api/`

| Endpoint | Method | Description | Auth Required |
|----------|---------|-------------|---------------|
| `/cart/` | GET | View cart contents | Yes |
| `/cart/items/` | POST | Add item to cart | Yes |
| `/cart/items/` | DELETE | Remove item from cart | Yes |
| `/orders/` | GET | List user's orders | Yes |
| `/orders/` | POST | Create new order from cart | Yes |
| `/orders/{id}/` | GET | Get order details | Yes |
| `/orders/{id}/status/` | PATCH | Update order status (Admin) | Admin |

### 🔔 WebSocket Notifications
**Endpoint:** `ws://localhost:8000/ws/notifications/`

Connect with a valid JWT token to receive real-time order status updates.

**Message Format:**
```json
{
  "type": "order_update",
  "order_id": 123,
  "status": "shipped",
  "message": "Your order has been shipped"
}
```

## 🧪 Testing

Run the complete test suite with coverage:

```bash
pytest --cov --cov-report=html
```

**Test Structure:**
- `core/tests/` - Authentication & user management tests
- `products/tests/` - Product model & API view tests
- `orders/tests/` - Cart, orders & WebSocket functionality tests

**View coverage report:**
```bash
# macOS
open htmlcov/index.html

# Windows
start htmlcov/index.html
```

## 🚀 Deployment

### Production Environment Setup

Update your `.env` file for production:

```env
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### Recommended Production Stack
- **Application Server:** Gunicorn/Uvicorn + Nginx
- **Database:** PostgreSQL
- **Caching:** Redis
- **WebSockets:** Daphne

### Sample Nginx Configuration

```nginx
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
```

## 🛠 Troubleshooting

### Redis Connection Issues
- Ensure Redis server is running: `redis-server`
- Check Redis version (requires 5.0+): `redis-server --version`
- Verify Redis URL in your environment settings

### Database Connection Problems
- Confirm PostgreSQL service is running
- Verify database credentials in `.env` file
- Run migrations if there are schema changes: `python manage.py migrate`

### WebSocket Connection Issues
- Ensure Daphne server is running for WebSocket support
- Check Redis configuration for channels layer
- Verify proxy configuration for WebSocket connections

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork** the project
2. **Create** your feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

**Built with ❤️ using Django REST Framework**

For questions or support, please open an issue or contact the maintainers.
