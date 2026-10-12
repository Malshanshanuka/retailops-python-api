
from fastapi import FastAPI

app = FastAPI(
    title="RetailOps API",
    description="Retail Inventory and Sales Management API",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "message": "Welcome to RetailOps API",
        "status": "running"
    }


@app.get("/products")
def get_products():
    products = [
        {"id": 1, "name": "Laptop", "price": 250000},
        {"id": 2, "name": "Mouse", "price": 3500},
        {"id": 3, "name": "Keyboard", "price": 7500}
    ]

    return products

