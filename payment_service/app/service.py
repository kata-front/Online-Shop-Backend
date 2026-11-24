import asyncio
from uuid import UUID

from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

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

    async def create_payment(self, payload: PaymentCreateSchema) -> PaymentReadSchema:
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

        return PaymentReadSchema.model_validate(payment)

    async def confirm_payment(self):
        await asyncio.sleep(4)