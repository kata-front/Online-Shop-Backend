from uuid import UUID

from fastapi import HTTPException
from starlette import status

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from .clients.catalog_client import CatalogClient
from .schemas import OrderCreateSchema, OrderReadSchema, OrderItemReadSchema
from .models import OrderItem, OrderORM

class OrderService:
    def __init__(
            self, 
            db: AsyncSession, 
            catalog_client: CatalogClient
        ):
        self.db = db
        self.catalog_client = catalog_client

    async def get_orders(self) -> list[OrderReadSchema]:
        orders = (await self.db.scalars(
            select(OrderORM).options(selectinload(OrderORM.items))
        )).all()
        return [OrderReadSchema.model_validate(order) for order in orders]

    async def get_order_by_id(self, id: UUID) -> OrderReadSchema:
        order = (await self.db.scalars(
            select(OrderORM)
            .options(selectinload(OrderORM.items))
            .where(OrderORM.id == id)
        )).one_or_none()

        if order is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

        return OrderReadSchema.model_validate(order)

    async def create_order(self, payload: OrderCreateSchema) -> OrderReadSchema:
        products: list[dict] = []

        for item in payload.items:
            product = await self.catalog_client.get_product(item.product_id)

            if 'detail' in product:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

            products.append({
                'product_id': item.product_id,
                'product_name': product['name'],
                'quantity': item.quantity,
                'unit_price': product['price']
            })

        order = OrderORM(
            user_id=payload.user_id,
            total_amount=sum([item['unit_price'] * item['quantity'] for item in products])
        )

        self.db.add(order)
        await self.db.flush()

        for item in products:
            self.db.add(OrderItem(order_id=order.id, **item))

        await self.db.commit()

        return OrderReadSchema(
            id=order.id,
            status=order.status,
            user_id=order.user_id,
            total_amount=order.total_amount,
            created_at=order.created_at,
            items=[
                OrderItemReadSchema(
                    order_id=order.id,
                    **item
                )
                for item in products
            ]
        )