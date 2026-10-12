from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import DateTime, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    category: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    price: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )

    low_stock_threshold: Mapped[int] = mapped_column(
        Integer,
        default=5,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

class Sale(Base):
    __tablename__ = "sales"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )

    product_id: Mapped[int] = mapped_column(
        Integer, nullable=False
    )

    quantity: Mapped[int] = mapped_column(
        Integer, nullable=False
    )

    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), nullable=False
    )

    total_amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )


