# alx-project-nexus
# ProDev BE: E-Commerce Backend

## Overview
A scalable backend for an e-commerce product catalog using Django, PostgreSQL, JWT auth, and Swagger docs. Supports CRUD for products/categories, filtering/sorting/pagination, and optimized queries.

## Tech Stack
- Django 5.x
- PostgreSQL
- djangorestframework + JWT
- drf-yasg (Swagger)

## Setup
1. Clone: `git clone git@github.com:innovation-gh/alx-project-nexus.git`
2. Install: `pip install -r requirements.txt`
3. Env vars: Add `SECRET_KEY`, `DATABASE_URL` (for local Postgres), `JWT_SECRET`.
4. Migrate: `python manage.py makemigrations && python manage.py migrate`
5. Run: `python manage.py runserver`
6. Docs: Visit `/api/docs` for Swagger.

## API Examples
- POST `/auth/login/`: User auth (JWT).
- GET `/products/?category=electronics&sort=price&limit=10`: Filtered/paginated list.

## ERD
[Embed image here from Step 2]

## Git Workflow
Follow conventional commits: `feat: add product CRUD`.