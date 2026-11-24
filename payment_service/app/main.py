from contextlib import asynccontextmanager
from uuid import UUID

from fastapi import Depends, FastAPI

from .schemas import PaymentCreateSchema, PaymentReadSchema
from .service import PaymentService
from .dependecies import get_payment_service
from .database import engine
from .models import Base

@asynccontextmanager
async def lifespan(_: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()

app = FastAPI(lifespan=lifespan)

@app.get('/payments', response_model=list[PaymentReadSchema])
async def get_payments(
    payment_service: PaymentService = Depends(get_payment_service)
):
    return await payment_service.get_payments()

@app.get('/payments/{id}', response_model=PaymentReadSchema)
async def get_payment(
    id: UUID,
    payment_service: PaymentService = Depends(get_payment_service)
):
    return await payment_service.get_by_id(id)

@app.post('/payments', response_model=PaymentReadSchema)
async def create_payment(
    payload: PaymentCreateSchema,
    payment_service: PaymentService = Depends(get_payment_service)
):
    payment = await payment_service.create_payment(payload)

    return PaymentReadSchema.model_validate(payment)