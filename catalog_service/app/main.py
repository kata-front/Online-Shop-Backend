from contextlib import asynccontextmanager
from uuid import UUID

from starlette import status

from fastapi import Depends, FastAPI, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import ProductCreateSchema, ProductReadSchema
from .dependencies import get_catalog_service
from .service import CatalogService
from .database import engine
from .models import Base

@asynccontextmanager
async def lifespan(_: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

    await engine.dispose()

app=FastAPI(
    lifespan=lifespan
)

@app.get('/products', response_model=list[ProductReadSchema])
async def get_products(catalog_service: CatalogService = Depends(get_catalog_service)):
    return await catalog_service.get_all_products()

@app.get('/product/{id}', response_model=ProductReadSchema)
async def get_product_by_id(id: UUID, catalog_service: CatalogService = Depends(get_catalog_service)):
    return await catalog_service.get_by_id(id)

@app.post(
    "/product", 
    response_model=ProductReadSchema,
    status_code=status.HTTP_201_CREATED
)
async def create_product(payload: ProductCreateSchema, catalog_service: CatalogService =Depends(get_catalog_service)):
    new_task = await catalog_service.create_product(payload)

    if new_task is None:
        raise HTTPException(status_code=409)

    return new_task