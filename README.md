<div align="center">

# 🛒 Django E-Commerce Platform

### A Modern Multi-Vendor E-Commerce Platform built with Django

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Django-5.x-092E20?style=for-the-badge&logo=django"/>
  <img src="https://img.shields.io/badge/Stripe-Payments-635BFF?style=for-the-badge&logo=stripe"/>
  <img src="https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite"/>
  <img src="https://img.shields.io/badge/Bootstrap-Frontend-7952B3?style=for-the-badge&logo=bootstrap"/>
</p>

A feature-rich multi-vendor eCommerce platform where **buyers** can browse and purchase products while **sellers** manage their own inventory through a dedicated dashboard.

---

</div>

# ✨ Features

## 👤 Authentication

- Custom User Model
- Buyer & Seller Roles
- User Registration & Login
- Profile Management
- Profile Picture Upload
- Address & Phone Management

---

## 🛍 Product Management

- Seller Dashboard
- Create Products
- Edit Products
- Delete Products
- Product Categories
- Product Images
- Inventory Management
- Stock Tracking

---

## 🛒 Shopping Cart

- Session-based Cart
- Logged-in User Cart
- Quantity Management
- Cart Persistence
- Automatic Total Calculation

---

## 💳 Checkout & Payments

- Stripe Checkout Integration
- Secure Payment Processing
- Order Confirmation
- Shipping Details
- Payment Success & Cancel Pages
- Stripe Webhook Support

---

## 📦 Orders

- Order Creation
- Order Items
- Order Status Tracking
- Inventory Reduction after Purchase
- Email Confirmation
- Order History Ready

---

## 📁 Project Structure

```
ecom/
│
├── accounts/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── decorators.py
│
├── shop/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│
├── cart/
│   ├── models.py
│   ├── views.py
│
├── orders/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│
├── templates/
├── static/
├── manage.py
└── requirements.txt
```

---

# 🏗 Database Design

```
CustomUser
│
├── Buyer
└── Seller
        │
        ▼
     Products
        │
        ▼
      Cart
        │
        ▼
    Cart Items
        │
        ▼
      Orders
        │
        ▼
    Order Items
```

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/m4shaikh/Ecommerce.git

cd Ecommerce
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

Activate

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment

Create a `.env` file or update your Django settings.

Example:

```env
SECRET_KEY=your-secret-key

DEBUG=True

STRIPE_SECRET_KEY=your_stripe_secret

STRIPE_WEBHOOK_SECRET=your_webhook_secret
```

---

## Run Migrations

```bash
python manage.py makemigrations

python manage.py migrate
```

---

## Create Superuser

```bash
python manage.py createsuperuser
```

---

## Start Development Server

```bash
python manage.py runserver
```

Open

```
http://127.0.0.1:8000/
```

---

# 🛠 Tech Stack

| Backend | Frontend | Database | Payments |
|----------|----------|-----------|-----------|
| Django | HTML | SQLite | Stripe |
| Python | CSS | Django ORM | Stripe Checkout |
| Django Authentication | Bootstrap | | |

---

# 🔄 Application Flow

```
User Registration
        │
        ▼
 Login
        │
        ▼
Buyer / Seller
      │
      ├──────────────┐
      ▼              ▼
 Browse Products   Seller Dashboard
      │              │
      ▼              ▼
 Add to Cart     Manage Products
      │
      ▼
 Checkout
      │
      ▼
 Stripe Payment
      │
      ▼
 Order Created
```

---

# 📸 Screenshots

Add screenshots here.

Suggested screenshots:

- Home Page
- Product Listing
- Product Details
- Shopping Cart
- Seller Dashboard
- Product Creation
- Checkout
- Stripe Payment
- User Profile

---

# Future Improvements

- Wishlist
- Product Reviews
- Search
- Coupons
- Discount Codes
- Order Tracking
- Admin Analytics
- Email Verification
- Password Reset
- Docker Support
- REST API
- Pagination

---

# 🤝 Contributing

Contributions are welcome.

1. Fork the repository

2. Create a new branch

```bash
git checkout -b feature/my-feature
```

3. Commit your changes

```bash
git commit -m "Added new feature"
```

4. Push

```bash
git push origin feature/my-feature
```

5. Open a Pull Request

---

# 📄 License

This project is licensed under the MIT License.

---

<div align="center">

### ⭐ If you like this project, don't forget to Star the repository!

Made with ❤️ using Django

</div>
