from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import ProductORM
from .schemas import ProductReadSchema, ProductCreateSchema

class CatalogService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_products(self) -> list[ProductReadSchema] | None:
        products = (await self.db.scalars(select(ProductORM))).all()

        return [ProductReadSchema.model_validate(product) for product in products]

    async def get_by_id(self, id: UUID) -> ProductReadSchema | None:
        product = await self.db.get(ProductORM, id)

        if product is None:
            return None

        return ProductReadSchema.model_validate(product)

    async def create_product(self, payload: ProductCreateSchema) -> ProductReadSchema:
        new_product = ProductORM(**payload.model_dump()) 
        self.db.add(new_product)     
        await self.db.commit()
        await self.db.refresh(new_product)

        return ProductReadSchema.model_validate(new_product)