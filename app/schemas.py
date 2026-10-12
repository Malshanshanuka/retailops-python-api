
from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict


class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    category: str = Field(min_length=1, max_length=50)
    price: Decimal = Field(gt=0, decimal_places=2)
    quantity: int = Field(ge=0)
    low_stock_threshold: int = Field(default=5, ge=0)


class ProductResponse(ProductCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


from datetime import datetime


class SaleCreate(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)


class SaleResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: Decimal
    total_amount: Decimal
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

