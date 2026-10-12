
# RetailOps API

A Python REST API for managing retail products, inventory, sales, and business analytics.

Built as a backend development portfolio project using FastAPI, SQLAlchemy, and SQLite.

## Features

- Product management with CRUD operations
- Inventory tracking and low-stock detection
- Sales recording with automatic stock reduction
- Insufficient-stock validation
- Sales revenue and quantity summaries
- Top-selling product analytics
- Interactive Swagger API documentation
- Automated API tests using Pytest

## Tech Stack

- Python 3.13
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Pytest
- Git and GitHub

## Project Structure

```text
retailops-python-api/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   └── schemas.py
├── tests/
│   └── test_products.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Malshanshanuka/retailops-python-api.git
cd retailops-python-api
```

### 2. Create a virtual environment

```bash
python3.13 -m venv .venv
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the application

```bash
python -m uvicorn app.main:app --reload
```

The API runs locally at:

http://127.0.0.1:8000

Swagger documentation:

http://127.0.0.1:8000/docs

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | API status |
| POST | /products | Create product |
| GET | /products | List products |
| GET | /products/{product_id} | Get product |
| PUT | /products/{product_id} | Update product |
| DELETE | /products/{product_id} | Delete product |
| GET | /inventory/low-stock | List low-stock products |
| POST | /sales | Record sale |
| GET | /sales | List sales |
| GET | /sales/{sale_id} | Get sale |
| GET | /analytics/summary | Sales summary |
| GET | /analytics/top-products | Top-selling products |

## Example: Create a Product

POST /products

Request:

```json
{
  "name": "Dell Laptop",
  "category": "Electronics",
  "price": "250000.00",
  "quantity": 10,
  "low_stock_threshold": 3
}
```

A successful request returns HTTP 201 Created.

## Sales and Inventory Logic

When a sale is recorded, the application:

1. Checks whether the product exists.
2. Validates the requested quantity.
3. Checks available stock.
4. Calculates the total sale value.
5. Saves the sale and updates inventory within a database transaction.

If available stock is insufficient, the API rejects the sale.

## Automated Testing

The project uses Pytest and FastAPI TestClient.

Run the tests:

```bash
python -m pytest -v
```

Seven automated tests currently cover product creation, retrieval, invalid prices, missing products, successful sales, insufficient stock, and analytics response structure.

## Current Limitations

This is a learning and portfolio project, not a production retail system.

It does not yet include user authentication, concurrency-safe stock reservations, or full accounting functionality.

## Future Improvements

- JWT authentication and role-based authorization
- PostgreSQL database support
- Docker containerization
- Improved concurrent sales handling
- CI/CD with GitHub Actions
- Additional integration tests

## Author

Malshan Shanuka

BSc (Hons) Information Technology, SLIIT

GitHub: https://github.com/Malshanshanuka
