from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Uuid, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)


class OrderItem(Base):
    __tablename__ = "order_items"

    order_id: Mapped[UUID] = mapped_column(
        ForeignKey("orders.id"),
        index=True,
    )
    product_id: Mapped[UUID]
    product_name: Mapped[str]
    quantity: Mapped[int]
    unit_price: Mapped[int]

    order: Mapped["OrderORM"] = relationship(
        "OrderORM", 
        back_populates="items",
    )


class OrderORM(Base):
    __tablename__ = "orders"

    status: Mapped[str] = mapped_column(default="Created")
    user_id: Mapped[UUID]
    total_amount: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    items: Mapped[list["OrderItem"]] = relationship(
        "OrderItem",
        back_populates="order",
    )