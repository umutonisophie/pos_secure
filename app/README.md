# POS System API

A backend REST API for a Point of Sale (POS) system, built with FastAPI, SQLAlchemy, and PostgreSQL. It supports product catalog management, inventory tracking, staff accounts, customer records, sales transactions with split payments, and receipt generation  designed for small to medium retail businesses (supermarkets, convenience stores, pharmacies, restaurant counters).

## Features

- Product catalog with categories and suppliers
- Real-time stock/inventory tracking, automatically deducted on sale
- Staff accounts with role-based access (Admin, Manager, Cashier)
- Customer records with optional loyalty point tracking
- Sales transactions supporting multiple line items per sale
- Split payments (multiple payment methods per sale)
- Automatic receipt issuance
- Server-side price lookup and stock validation  prices and totals are never trusted from the client
- Relationship integrity enforcement (e.g. a sale item cannot reference a product that doesn't exist)

## Tech Stack

- **Framework:** FastAPI
- **ORM:** SQLAlchemy
- **Database:** PostgreSQL
- **Validation:** Pydantic
- **Password hashing:** Passlib (bcrypt)

## Project Structure

app/
├── models/ # SQLAlchemy ORM models (one file per entity)
├── schemas/ # Pydantic request/response schemas
├── repository/ # Data access layer (CRUD against the DB)
├── services/ # Business logic (validation, orchestration, stock/price rules)
├── routers/ # FastAPI route definitions (HTTP layer)
├── database.py # DB engine, session, and dependency injection
└── main.py # FastAPI app entrypoint, router registration


The architecture follows a layered flow:
**Router → Service → Repository → Model**
Routers stay thin (no business logic). Services hold all business rules — including 404 handling, price/stock lookups, and relationship validation. Repositories handle raw CRUD. Models define the database schema.

## Data Model

The system has 9 entities:

| Entity | Description |
|---|---|
| Category | Product categories |
| Supplier | Product suppliers |
| Product | Catalog items, stock, pricing |
| User | Staff accounts (Admin/Manager/Cashier) |
| Customer | Customer records, loyalty points |
| Sale | A completed transaction |
| SaleItem | Line items within a sale (product + quantity) |
| Payment | Payment(s) applied to a sale (supports splits) |
| Receipt | Proof-of-purchase issued for a sale |

Key relationships:
- Category → Product (one-to-many)
- Supplier → Product (one-to-many)
- Customer → Sale (one-to-many)
- User → Sale (one-to-many, the cashier who processed it)
- Sale → SaleItem (one-to-many)
- Sale → Payment (one-to-many, supports split payments)
- Sale → Receipt (one-to-one)
- Product :left_right_arrow: Sale (many-to-many, resolved through SaleItem)

## Setup Instructions

### 1. Clone the repository

```bash
git clone git@github.com:marymachariam/pos-system.git
cd pos-system
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv env
source env/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up PostgreSQL

Create the database:

```bash
createdb pos_db
```

or via `psql`:

```sql
CREATE DATABASE pos_db;
```

### 5. Configure environment variables

Create a `.env` file inside the `app/` directory:

DATABASE_URL=postgresql://postgres:postgres@localhost:5432/pos_db


Adjust the username, password, host, and port to match your local PostgreSQL setup.

### 6. Run the application

```bash
cd app
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.
Tables are created automatically on startup.

### 7. Explore the API

Open the interactive Swagger docs at:

http://127.0.0.1:8000/docs


## API Endpoints

All endpoints support standard REST operations (`GET`, `POST`, `PUT`, `DELETE`) unless noted otherwise.

| Resource | Base Path |
|---|---|
| Categories | `/categories` |
| Suppliers | `/suppliers` |
| Products | `/products` |
| Users | `/users` |
| Customers | `/customers` |
| Sales | `/sales` |
| Sale Items | `/sale-items` |
| Payments | `/payments` |
| Receipts | `/receipts` |

**Checkout flow:** `POST /sales/` accepts a nested payload of `sale_items` and `payments` in a single request. The server:
1. Looks up each product's real price and confirms stock is available
2. Deducts stock
3. Calculates subtotal/tax/total from the actual line items (never trusts client-submitted totals)
4. Validates that submitted payments sum to the total
5. Generates a unique sale number
6. Commits the sale, its items, and its payments atomically

## Running Tests

The project uses **pytest** with an in-memory SQLite database (isolated from the development PostgreSQL database) to run a comprehensive automated test suite.

### 1. Set up the virtual environment (if not already done)

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
pip install pytest
```

### 2. Run the full test suite

```bash
cd app
python -m pytest tests/ -v
```

### 3. Run tests for a specific module

```bash
# Run tests for a specific entity
python -m pytest tests/test_product.py -v
python -m pytest tests/test_category.py -v
python -m pytest tests/test_customer.py -v
python -m pytest tests/test_supplier.py -v
python -m pytest tests/test_sale.py -v
python -m pytest tests/test_sale_item.py -v
python -m pytest tests/test_payment.py -v
python -m pytest tests/test_receipt.py -v
python -m pytest tests/test_user.py -v
python -m pytest tests/test_auth.py -v
```

### 4. Run tests with coverage (optional)

```bash
pip install pytest-cov
python -m pytest tests/ --cov=app --cov-report=term-missing
```

### Test Suite Overview

The test suite covers all major entities and features:

| Test File | Coverage |
|-----------|----------|
| `test_auth.py` | User registration, login, token validation |
| `test_category.py` | CRUD + validation + 404 + auth |
| `test_customer.py` | CRUD + validation + 404 + auth |
| `test_supplier.py` | CRUD + validation + 404 + auth |
| `test_product.py` | CRUD + foreign key validation (category, supplier) + 404 + auth |
| `test_sale.py` | CRUD + foreign key validation (user, customer) + 404 + auth |
| `test_sale_item.py` | CRUD + foreign key validation (sale, product) + 404 + auth |
| `test_payment.py` | CRUD + foreign key validation (sale) + 404 + auth |
| `test_receipt.py` | CRUD + foreign key validation (sale) + unique receipt_number + 404 + auth |
| `test_user.py` | CRUD + password update + duplicate username + 404 + auth |

All tests use fixtures defined in `tests/conftest.py`:
- `client` - TestClient with isolated SQLite database
- `test_user` - Creates a test user for authentication
- `auth_headers` - Bearer token for authenticated requests

The test database is created fresh for each test function and destroyed afterward, ensuring complete isolation.

## Security Notes

- Passwords are hashed with bcrypt before storage; the `password_hash` field is never exposed in API responses.
- Prices and totals for sales are always computed server-side, never accepted directly from the client.
- Database credentials are stored in a `.env` file, excluded from version control via `.gitignore`.

## Author
Sophie Umutoni# POS