import asyncio
from uuid import UUID, uuid4

from aio_pika.abc import AbstractExchange

from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .config import settings
from .rabbitmq import publish_json
from .clients.order_client import OrderClient
from .models import PaymentORM
from .schemas import PaymentReadSchema, PaymentCreateSchema

class PaymentService:
    def __init__(
        self, 
        db: AsyncSession,
        order_client: OrderClient
    ):
        self.db = db
        self.order_client = order_client

    async def get_payments(self) -> list[PaymentReadSchema]:
        payments = (await self.db.scalars(
            select(PaymentORM)
        )).all()

        return [PaymentReadSchema.model_validate(payment) for payment in payments]

    async def get_by_id(self, id: UUID) -> PaymentReadSchema:
        payment = await self.db.get(PaymentORM, id)

        if payment is None:
            raise HTTPException(status_code=404)

        return PaymentReadSchema.model_validate(payment)

    async def create_payment(self, payload: PaymentCreateSchema) -> PaymentORM:
        order = await self.order_client.get_order(payload.order_id)

        if order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Order not found"
            )

        payment = PaymentORM(**payload.model_dump())

        self.db.add(payment)
        await self.db.commit()

        await self.db.refresh(payment)

        return payment

    async def confirm_payment(
        self, 
        payment: PaymentORM,
        order_id: str,
        user_id: str,
        amount: str,
        exchange: AbstractExchange
    ):
        await asyncio.sleep(4)

        payment.status = 'suceeded'
        await self.db.commit()

        event = {
            'event_id': str(uuid4()),
            'order_id': order_id,
            'status': 'succeeded',
            'amount': amount,
            'user_id': user_id
        }

        await publish_json(exchange, settings.payment_succeeded_routimg_key, event)