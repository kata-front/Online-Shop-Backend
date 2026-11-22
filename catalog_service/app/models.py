from uuid import uuid4

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Uuid

class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(
        Uuid, 
        primary_key=True, 
        default=lambda: uuid4()
    )

class ProductORM(Base):
    __tablename__="products"

    name: Mapped[str]
    price: Mapped[int]
    description: Mapped[str]