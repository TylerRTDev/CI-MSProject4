# 🎵 Real Legacy Media

## Table of Contents

- [📦 Project Overview](#-project-overview)
- [💡 Rationale](#-rationale)
- [🎯 Objectives](#-objectives)
- [👥 User Stories](#-user-stories)
- [🌟 Key Features](#-key-features)
- [🚀 Getting Started](#-getting-started)
- [🛠️ Technologies Used](#-technologies-used)
- [📚 Usage Instructions](#-usage-instructions)
- [🧪 Testing and Deployment](#-testing-and-deployment)
- [🤝 Contributing](#-contributing)
- [🙏 Credits and Acknowledgements](#-credits-and-acknowledgements)
- [📄 License](#-license)
- [🐞 Known Issues & Future Improvements](#-known-issues--future-improvements)
- [📷 Screenshots](#-screenshots)



## 📦 Project Overview

Welcome to **Real Legacy Media**, a full-stack Django-powered e-commerce platform built for music lovers, collectors, and creators. Whether you're hunting for rare vinyl, stocking up on CDs, or browsing for digital downloads and exclusive merchandise, this app lets you do it all in a streamlined, stylish, and secure environment.

Designed to feel like a record store reimagined for the web, Real Legacy Media supports a smooth customer experience and includes powerful administrative tools for managing inventory, users, and orders. From casual visitors to returning shoppers and site admins, every user role is thoughtfully supported.

---

## 💡 Rationale

Music is timeless—but the way people discover and purchase it is constantly evolving. Real Legacy Media taps into the resurgence of physical music formats, while offering the convenience of a modern online storefront. The project was born from a desire to:

* Blend the nostalgic appeal of record shops with modern UX/UI practices
* Create a community-focused platform that supports browsing, reviewing, and collecting
* Provide admin-level control without compromising frontend design or user experience

---

## 🎯 Objectives

This project is designed to meet both business and technical goals. Your objectives as a developer or stakeholder are to:

* Deploy a full-featured e-commerce app using Django
* Implement secure user authentication and profile management
* Enable browsing, filtering, and purchasing of media in multiple formats
* Support a clean admin interface with CRUD functionality for products and orders
* Prioritise responsive design, accessible navigation, and strong visual identity

---

## 👥 User Stories

### 🎧 As a Music Fan (Site Visitor):

* You can browse music by genre, artist, or format.
* You can preview albums or tracks (if previews are enabled).
* You can view product details including images, pricing, and stock status.
* You can create an account to track orders and manage your information.

### 🛒 As a Returning Customer:

* You can log in to view your past orders.
* You can easily reorder previously purchased items.
* You can update your password and profile information.
* You can save favorite items to a wishlist (planned feature).

### 🧑‍💼 As a Site Admin:

* You can manage product listings, images, and stock levels.
* You can add and edit categories, genres, or media types.
* You can view and update customer orders and shipping details.
* You can mark items as "Featured" or "Limited Edition."

---

## 🌟 Key Features

* **Dynamic Product Catalogue**: View products by category, genre, and type with sorting and search filters.
* **User Authentication**: Secure sign-up, login, logout, and profile editing features.
* **Shopping Cart**: Add, update, and remove items in your cart. Select sizes/formats if applicable.
* **Order Management**: Logged-in users can view order summaries, track delivery status, and re-order items.
* **Stripe Checkout**: Integrated payment gateway using Stripe’s test mode for secure transactions.
* **Responsive Design**: Optimised for mobile, tablet, and desktop experiences.
* **Admin Dashboard**: Fully featured backend interface for managing products, orders, users, and site content.

---

## 🚀 Getting Started

To run this project locally, follow the steps below. These instructions assume you're using Python 3.10+ and have `pip` and `git` installed.

### 🔧 Prerequisites

* Python 3.10+
* pip
* Git
* Virtual environment tool (e.g., `venv` or `virtualenv`)
* \[Optional] PostgreSQL for production use

### 📦 Installation Steps

1. **Clone the repository**

```bash
git clone https://github.com/your-username/real-legacy-media.git
cd real-legacy-media
```

2. **Create and activate a virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
   Create a `.env` file in the root directory with the following keys:

```
SECRET_KEY=your_django_secret_key
STRIPE_PUBLISHABLE_KEY=your_stripe_test_key
STRIPE_SECRET_KEY=your_stripe_secret_key
DEBUG=True
```

5. **Apply database migrations**

```bash
python manage.py migrate
```

6. **Create a superuser for admin access**

```bash
python manage.py createsuperuser
```

7. **Run the development server**

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser to view the site.

---

## 🛠️ Technologies Used

### 💻 Backend

* Django 4.x (Python Web Framework)
* SQLite (default development DB)
* PostgreSQL (recommended for production)
* Python Decouple (for environment variable management)

### 🎨 Frontend

* Django Templates
* Bootstrap 5 (Responsive CSS Framework)
* Custom CSS and JavaScript enhancements

### 🧾 Payments & Accounts

* Stripe API (sandbox test mode enabled)
* Django’s built-in auth system (login, logout, password change)

### ⚙️ Tooling & Deployment

* Git & GitHub for version control
* Render.com (for deployment)
* Pillow (for image upload handling)
* Crispy Forms + Bootstrap 5 for styled form rendering

---

## 📚 Usage Instructions

### For Shoppers

* **Browse** music by category, genre, or type using the top navigation or filters.
* **View product details** including title, format, pricing, availability, and description.
* **Add to Cart**: Choose the format or size, then add the item to your cart.
* **Checkout**: Review cart items and complete payment securely via Stripe.
* **Order History**: Log in to view all your past purchases and order details.
* **Profile Management**: Update your personal details, address, and contact info.

### For Admins

* **Access Django Admin** via `/admin/` with your superuser credentials.
* **Manage Products**: Add/edit/delete items, upload images, set stock levels.
* **Track Orders**: Update order status (e.g., pending, shipped, delivered).
* **User & Category Management**: Edit user profiles, create new genres or categories.

---

## 🧪 Testing and Deployment

### ✅ Testing

Testing includes both automated and manual verification across key user workflows.

* **Unit Tests**: Run with Django’s built-in test suite:

```bash
python manage.py test
```

* **Manual Testing**: Performed on:

  * User registration and login
  * Cart interactions (add/update/remove)
  * Order placement and confirmation
  * Admin views and CRUD operations
  * Mobile and tablet responsiveness

> Using tools like Postman for API endpoint validation or pytest for extended test coverage.

### 🚀 Deployment

The app is deployed to [Render](https://render.com/) with the following setup:

* **Web Server**: Gunicorn (or `manage.py runserver` for dev)
* **Environment Variables**: Managed via `.env` (in development) and dashboard settings in Render
* **Database**: SQLite in development; PostgreSQL or other production-ready DB recommended
* **Static/Media Files**:

  ```bash
  python manage.py collectstatic
  ```
* **Domains & HTTPS**: Use Render’s domain setup or custom domain configuration for production readiness

---

## 🐞 Known Issues & Future Improvements

While the core features of Real Legacy Media are fully functional, the following improvements and features are planned:

* 🧾 **Coupon Support**: Backend model and checkout logic for promotional discounts.
* 💖 **Wishlist System**: Model exists but frontend logic is incomplete (planned for Phase 2).
* 🔊 **Audio Previews**: HTML5 player integration for music sample previews.
* 🔔 **Email Notifications**: Order confirmation and shipping updates via email (currently console-based).
* 🧑‍🤝‍🧑 **Subscriptions & Rewards**: Membership plans, exclusive drops, and subscriber perks.
* 🔍 **Enhanced Search & Filtering**: More granular filtering by artist, format, price range.
* 📱 **Progressive Web App Support**: For an installable, app-like experience.

If you're interested in contributing to these features, see the Contributing section.

---
