from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class OrderItemReadSchema(BaseModel):
    order_id: UUID
    product_id: UUID
    product_name: str
    quantity: int
    unit_price: int

    model_config = ConfigDict(from_attributes=True)

class OrderItemCreateSchema(BaseModel):
    product_id: UUID
    quantity: int
    unit_price: int

class OrderCreateSchema(BaseModel):
    total_amount: int
    user_id: UUID

    items: list[OrderItemCreateSchema]

class OrderReadSchema(BaseModel):
    id: UUID
    status: str
    user_id: UUID
    total_amount: int
    created_at: datetime

    items: list[OrderItemReadSchema]

    model_config = ConfigDict(from_attributes=True)
