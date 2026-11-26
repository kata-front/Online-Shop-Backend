import json

import aio_pika
from aio_pika.abc import  AbstractConnection, AbstractExchange, AbstractIncomingMessage, AbstractRobustConnection

from .models import OrderORM
from .database import SessionLocal
from .config import settings

async def connect_rabbitmq(url: str) -> AbstractRobustConnection:
    return await aio_pika.connect_robust(url)

async def handle_payment_events(message: AbstractIncomingMessage):
    async with message.process():
        event = json.loads(message.body.decode('utf-8'))
        async with SessionLocal() as session:
            order = await session.get(OrderORM, event['order_id']) 

            if order is not None:
                order.status = 'paid'
                await session.commit()


async def start_payments_consume(connection: AbstractConnection):
    channel = await connection.channel()
    exchange = await channel.declare_exchange(
        settings.payment_exchange_name
    )
    queue = await channel.declare_queue(settings.payment_queue_name)

    await queue.bind(exchange, settings.payment_succeeded_routimg_key)
    await queue.consume(handle_payment_events)