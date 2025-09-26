# alx-project-nexus
# alx-project-nexus

# E-Commerce API Documentation

## Overview

This API provides endpoints for managing an e-commerce platform, including user management, product catalog, shopping cart, and order processing functionality.

**Base URL:** `https://alx-project-nexus-o9nx.onrender.com/api`

**API Documentation:** [Interactive Docs](https://alx-project-nexus-o9nx.onrender.com/api/docs/)

## Table of Contents

- [Authentication](#authentication)
- [User Management](#user-management)
- [Product Management](#product-management)
- [Cart Management](#cart-management)
- [Order Management](#order-management)
- [Categories](#categories)
- [Error Handling](#error-handling)
- [Rate Limiting](#rate-limiting)

## Authentication

Most endpoints require authentication. Include the authorization token in your request headers:

```
Authorization: Bearer YOUR_TOKEN_HERE
```

### Login

```http
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**

```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

### Register

```http
POST /auth/register
Content-Type: application/json

{
  "name": "John Doe",
  "email": "user@example.com",
  "password": "password123"
}
```

## User Management

### Get User Profile

```http
GET /users/profile
Authorization: Bearer YOUR_TOKEN_HERE
```

### Update User Profile

```http
PUT /users/profile
Authorization: Bearer YOUR_TOKEN_HERE
Content-Type: application/json

{
  "name": "John Smith",
  "email": "johnsmith@example.com",
  "phone": "+1234567890"
}
```

## Product Management

### Get All Products

```http
GET /products?page=1&limit=10&category=electronics&sort=price&order=asc
```

**Query Parameters:**

- `page` (optional): Page number (default: 1)
- `limit` (optional): Number of items per page (default: 10)
- `category` (optional): Filter by category
- `sort` (optional): Sort by field (name, price, created_at)
- `order` (optional): Sort order (asc, desc)
- `search` (optional): Search term

**Response:**

```json
{
  "products": [
    {
      "id": 1,
      "name": "iPhone 15",
      "description": "Latest iPhone model",
      "price": 999.99,
      "category": "electronics",
      "image_url": "https://example.com/image.jpg",
      "in_stock": true,
      "quantity": 50
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 5,
    "total_items": 50,
    "items_per_page": 10
  }
}
```

### Get Product by ID

```http
GET /products/{id}
```

### Create Product (Admin)

```http
POST /products
Authorization: Bearer ADMIN_TOKEN
Content-Type: application/json

{
  "name": "New Product",
  "description": "Product description",
  "price": 29.99,
  "category_id": 1,
  "image_url": "https://example.com/image.jpg",
  "quantity": 100
}
```

### Update Product (Admin)

```http
PUT /products/{id}
Authorization: Bearer ADMIN_TOKEN
Content-Type: application/json

{
  "name": "Updated Product Name",
  "price": 39.99
}
```

### Delete Product (Admin)

```http
DELETE /products/{id}
Authorization: Bearer ADMIN_TOKEN
```

## Cart Management

### Get Cart

```http
GET /cart
Authorization: Bearer YOUR_TOKEN_HERE
```

**Response:**

```json
{
  "items": [
    {
      "id": 1,
      "product": {
        "id": 1,
        "name": "iPhone 15",
        "price": 999.99,
        "image_url": "https://example.com/image.jpg"
      },
      "quantity": 2,
      "subtotal": 1999.98
    }
  ],
  "total": 1999.98,
  "item_count": 2
}
```

### Add Item to Cart

```http
POST /cart/items
Authorization: Bearer YOUR_TOKEN_HERE
Content-Type: application/json

{
  "product_id": 1,
  "quantity": 2
}
```

### Update Cart Item

```http
PUT /cart/items/{item_id}
Authorization: Bearer YOUR_TOKEN_HERE
Content-Type: application/json

{
  "quantity": 3
}
```

### Remove Item from Cart

```http
DELETE /cart/items/{item_id}
Authorization: Bearer YOUR_TOKEN_HERE
```

### Clear Cart

```http
DELETE /cart
Authorization: Bearer YOUR_TOKEN_HERE
```

## Order Management

### Get Orders

```http
GET /orders?status=pending&page=1&limit=10
Authorization: Bearer YOUR_TOKEN_HERE
```

### Get Order by ID

```http
GET /orders/{id}
Authorization: Bearer YOUR_TOKEN_HERE
```

### Create Order

```http
POST /orders
Authorization: Bearer YOUR_TOKEN_HERE
Content-Type: application/json

{
  "shipping_address": {
    "street": "123 Main St",
    "city": "New York",
    "state": "NY",
    "zip_code": "10001",
    "country": "USA"
  },
  "payment_method": "credit_card"
}
```

**Response:**

```json
{
  "id": 1,
  "status": "pending",
  "total": 1999.98,
  "items": [...],
  "shipping_address": {...},
  "created_at": "2023-12-01T10:00:00Z"
}
```

### Update Order Status (Admin)

```http
PUT /orders/{id}/status
Authorization: Bearer ADMIN_TOKEN
Content-Type: application/json

{
  "status": "shipped"
}
```

## Categories

### Get All Categories

```http
GET /categories
```

**Response:**

```json
{
  "categories": [
    {
      "id": 1,
      "name": "Electronics",
      "description": "Electronic devices and accessories"
    },
    {
      "id": 2,
      "name": "Clothing",
      "description": "Fashion and apparel"
    }
  ]
}
```

### Create Category (Admin)

```http
POST /categories
Authorization: Bearer ADMIN_TOKEN
Content-Type: application/json

{
  "name": "Books",
  "description": "Books and literature"
}
```

## Error Handling

The API uses standard HTTP status codes and returns error details in JSON format:

```json
{
  "error": "Validation Error",
  "message": "Invalid email format",
  "details": {
    "field": "email",
    "code": "INVALID_FORMAT"
  }
}
```

### Common Status Codes

- `200 OK` - Request successful
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `422 Unprocessable Entity` - Validation error
- `500 Internal Server Error` - Server error

## Rate Limiting

The API implements rate limiting to ensure fair usage:

- **Authenticated users**: 1000 requests per hour
- **Guest users**: 100 requests per hour

Rate limit headers are included in responses:

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
```

## Example Usage

### JavaScript/Node.js Example

```javascript
const API_BASE_URL = "https://alx-project-nexus-o9nx.onrender.com/api";

// Login and get token
async function login(email, password) {
  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, password }),
  });

  const data = await response.json();
  return data.token;
}

// Get products
async function getProducts(token) {
  const response = await fetch(`${API_BASE_URL}/products`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  return await response.json();
}

// Add item to cart
async function addToCart(token, productId, quantity) {
  const response = await fetch(`${API_BASE_URL}/cart/items`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      product_id: productId,
      quantity: quantity,
    }),
  });

  return await response.json();
}
```

### Python Example

```python
import requests

API_BASE_URL = 'https://alx-project-nexus-o9nx.onrender.com/api'

class ECommerceAPI:
    def __init__(self):
        self.token = None
        self.session = requests.Session()

    def login(self, email, password):
        response = self.session.post(f'{API_BASE_URL}/auth/login',
                                   json={'email': email, 'password': password})
        data = response.json()
        self.token = data['token']
        self.session.headers.update({'Authorization': f'Bearer {self.token}'})
        return data

    def get_products(self, **params):
        response = self.session.get(f'{API_BASE_URL}/products', params=params)
        return response.json()

    def add_to_cart(self, product_id, quantity):
        response = self.session.post(f'{API_BASE_URL}/cart/items',
                                   json={'product_id': product_id, 'quantity': quantity})
        return response.json()

# Usage
api = ECommerceAPI()
api.login('user@example.com', 'password123')
products = api.get_products(category='electronics', limit=5)
```

## Support

For questions or issues with the API, please:

1. Check the [interactive documentation](https://alx-project-nexus-o9nx.onrender.com/api/docs/)
2. Review this README for common use cases
3. Open an issue in this repository

## Contributing

We welcome contributions! Please read our contributing guidelines and submit pull requests for any improvements.

---

**Note:** This documentation is based on common e-commerce API patterns. Please refer to the [interactive API documentation](https://alx-project-nexus-o9nx.onrender.com/api/docs/) for the most up-to-date and accurate endpoint specifications.
