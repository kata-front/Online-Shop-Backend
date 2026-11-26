from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class PaymentReadSchema(BaseModel):
    id: UUID
    order_id: UUID
    user_id: UUID
    status: str
    amount: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class PaymentCreateSchema(BaseModel):
    order_id: UUID
    amount: int
    user_id: UUID