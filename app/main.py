
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Product
from app.schemas import ProductCreate, ProductResponse
from app.models import Product
from app.schemas import ProductCreate, ProductResponse
from app.models import Product, Sale
from app.schemas import (
    ProductCreate,
    ProductResponse,
    SaleCreate,
    SaleResponse
)

Base.metadata.create_all(bind=engine)

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


@app.post("/products", response_model=ProductResponse, status_code=201)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    new_product = Product(**product.model_dump())

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


@app.get("/products", response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = db.get(Product, product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product


@app.put("/products/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    updated_data: ProductCreate,
    db: Session = Depends(get_db)
):
    product = db.get(Product, product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    for key, value in updated_data.model_dump().items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)

    return product

@app.delete("/products/{product_id}", status_code=204)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = db.get(Product, product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    db.delete(product)
    db.commit()


@app.get("/inventory/low-stock",
         response_model=list[ProductResponse])
def get_low_stock_products(
    db: Session = Depends(get_db)
):
    low_stock_products = db.query(Product).filter(
        Product.quantity <= Product.low_stock_threshold
    ).all()

    return low_stock_products


@app.post("/sales", response_model=SaleResponse, status_code=201)
def create_sale(
    sale_data: SaleCreate,
    db: Session = Depends(get_db)
):
    product = db.get(Product, sale_data.product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    if product.quantity < sale_data.quantity:
        raise HTTPException(
            status_code=400,
            detail="Insufficient stock"
        )

    total = product.price * sale_data.quantity

    new_sale = Sale(
        product_id=product.id,
        quantity=sale_data.quantity,
        unit_price=product.price,
        total_amount=total
    )

    product.quantity -= sale_data.quantity

    db.add(new_sale)

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

    db.refresh(new_sale)

    return new_sale


@app.get("/sales", response_model=list[SaleResponse])
def get_sales(db: Session = Depends(get_db)):
    return db.query(Sale).all()


@app.get("/sales/{sale_id}", response_model=SaleResponse)
def get_sale(
    sale_id: int,
    db: Session = Depends(get_db)
):
    sale = db.get(Sale, sale_id)

    if sale is None:
        raise HTTPException(
            status_code=404,
            detail="Sale not found"
        )

    return sale


