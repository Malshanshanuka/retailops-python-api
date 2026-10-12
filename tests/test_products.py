
import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db


# Create a separate in-memory test database
test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestSession = sessionmaker(bind=test_engine)


@pytest.fixture
def client():
    Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        db = TestSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=test_engine)


def test_create_product(client):
    response = client.post(
        "/products",
        json={
            "name": "Dell Laptop",
            "category": "Electronics",
            "price": "250000.00",
            "quantity": 10,
            "low_stock_threshold": 3
        }
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Dell Laptop"
    assert response.json()["quantity"] == 10


def test_get_products(client):
    response = client.get("/products")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_invalid_product_price(client):
    response = client.post(
        "/products",
        json={
            "name": "Mouse",
            "category": "Accessories",
            "price": "-500.00",
            "quantity": 5,
            "low_stock_threshold": 2
        }
    )

    assert response.status_code == 422


def test_product_not_found(client):
    response = client.get("/products/9999")

    assert response.status_code == 404


def test_successful_sale_reduces_stock(client):
    # Step 1: Create a product with 10 items
    product_response = client.post(
        "/products",
        json={
            "name": "Dell Laptop",
            "category": "Electronics",
            "price": "250000.00",
            "quantity": 10,
            "low_stock_threshold": 3
        }
    )

    assert product_response.status_code == 201

    product_id = product_response.json()["id"]

    # Step 2: Sell 2 items
    sale_response = client.post(
        "/sales",
        json={
            "product_id": product_id,
            "quantity": 2
        }
    )

    assert sale_response.status_code == 201
    assert sale_response.json()["quantity"] == 2
    assert sale_response.json()["total_amount"] == "500000.00"

    # Step 3: Check remaining stock
    stock_response = client.get(
        f"/products/{product_id}"
    )

    assert stock_response.status_code == 200
    assert stock_response.json()["quantity"] == 8


def test_insufficient_stock(client):
    # Step 1: Create a product with 5 items
    product_response = client.post(
        "/products",
        json={
            "name": "Wireless Mouse",
            "category": "Accessories",
            "price": "3500.00",
            "quantity": 5,
            "low_stock_threshold": 2
        }
    )

    product_id = product_response.json()["id"]

    # Step 2: Attempt to sell 20 items
    response = client.post(
        "/sales",
        json={
            "product_id": product_id,
            "quantity": 20
        }
    )

    # Step 3: Verify rejection
    assert response.status_code == 400
    assert response.json()["detail"] == "Insufficient stock"

    # Step 4: Ensure stock is unchanged
    stock_response = client.get(
        f"/products/{product_id}"
    )

    assert stock_response.json()["quantity"] == 5


def test_sales_analytics(client):
    response = client.get("/analytics/summary")

    assert response.status_code == 200

    data = response.json()

    assert "total_revenue" in data
    assert "total_sales" in data
    assert "total_units_sold" in data
    assert "low_stock_products" in data

