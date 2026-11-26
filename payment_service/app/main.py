from contextlib import asynccontextmanager
from uuid import UUID

from fastapi import Depends, FastAPI, Request

from .rabbitmq import connect_rabbitmq, declare_payment_exchange
from .schemas import PaymentCreateSchema, PaymentReadSchema
from .service import PaymentService
from .dependecies import get_payment_service
from .database import engine
from .models import Base
from .config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    connection = await connect_rabbitmq(settings.rebbitmq_url)
    channel = await connection.channel()
    app.state.payment_exchange = await declare_payment_exchange(channel, settings.payment_exchange_name)

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
    request: Request,
    payload: PaymentCreateSchema,
    payment_service: PaymentService = Depends(get_payment_service)
):
    payment = await payment_service.create_payment(payload)

    await payment_service.confirm_payment(
        payment,
        str(payload.order_id),
        str(payload.user_id),
        str(payload.amount),
        request.app.state.payment_exchange
    )

    return PaymentReadSchema.model_validate(payment)