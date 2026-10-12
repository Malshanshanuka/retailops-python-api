
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
