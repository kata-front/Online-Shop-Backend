from pydantic import BaseModel, ConfigDict
from uuid import UUID

class ProductReadSchema(BaseModel):
    id: UUID
    name: str
    price: int
    description: str

    model_config = ConfigDict(from_attributes=True)

class ProductCreateSchema(BaseModel):
    name: str
    price: int
    description: str