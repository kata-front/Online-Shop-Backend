from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Uuid, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    id: Mapped[UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=lambda: uuid4()
    )

class PaymentORM(Base):
    __tablename__="payments"

    user_id: Mapped [UUID]
    order_id: Mapped[UUID]
    status: Mapped[str] = mapped_column(default='created')
    amount: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )