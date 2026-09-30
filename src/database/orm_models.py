from datetime import datetime

from sqlalchemy import (
    BigInteger,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.connection import Base


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    order_id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        nullable=False,
        index=True,
    )

    type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    customer_segment: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    customer_state: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    order_country: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    order_region: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    shipping_mode: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    total_quantity: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    total_discount: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    num_unique_products: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    num_unique_categories: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    num_unique_departments: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    order_hour: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    order_dayofweek: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    order_month: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    predictions: Mapped[list["Prediction"]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan",
    )


class Prediction(Base):
    __tablename__ = "predictions"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    order_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("orders.order_id"),
        nullable=False,
        index=True,
    )

    late_risk_probability: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    late_risk_prediction: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    risk_label: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    threshold: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    model_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    order: Mapped["Order"] = relationship(
        back_populates="predictions",
    )
