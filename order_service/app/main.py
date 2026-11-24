from contextlib import asynccontextmanager
from uuid import UUID

from fastapi import Depends, FastAPI

from starlette import status

from .dependecies import get_order_service
from .service import OrderService
from .schemas import OrderCreateSchema, OrderReadSchema
from .models import Base
from .database import engine

@asynccontextmanager
async def lifespan(_: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()


app = FastAPI(lifespan=lifespan)

@app.get('/orders', response_model=list[OrderReadSchema])
async def get_orders(
    order_service: OrderService = Depends(get_order_service)
):
    return await order_service.get_orders()

@app.get('/orders/{order_id}', response_model=OrderReadSchema)
async def get_order_by_id(
    order_id: UUID,
    order_service: OrderService = Depends(get_order_service) 
):
    return await order_service.get_order_by_id(order_id)

@app.post("/orders", response_model=OrderReadSchema, status_code=status.HTTP_201_CREATED)
async def create_new_product(
    payload: OrderCreateSchema,
    order_service: OrderService = Depends(get_order_service)
):
    return await order_service.create_order(payload)