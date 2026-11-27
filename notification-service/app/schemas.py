from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

class NotifReadSchema(BaseModel):
    id: UUID
    order_id: UUID
    user_id: UUID
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)