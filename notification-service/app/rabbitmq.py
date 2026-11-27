import json

import aio_pika
from aio_pika.abc import AbstractConnection, AbstractIncomingMessage

from .config import settings
from .database import SessionLocal
from .models import NotifORM

async def connect_rabbitmq(url: str):
    return await aio_pika.connect_robust(url)

async def handle_payment_events(message: AbstractIncomingMessage):
    async with message.process():
        event = json.loads(message.body.decode('utf-8'))
        async with SessionLocal() as session:
            new_notif = NotifORM(
                order_id=event['order_id'],
                user_id=event['user_id']
            )
            session.add(new_notif)
            await session.commit()

async def start_payments_consume(connection: AbstractConnection):
    channel = await connection.channel()
    exchange = await channel.declare_exchange(
        settings.payment_exchange_name
    )
    queue = await channel.declare_queue(settings.payment_queue_name)

    await queue.bind(exchange, settings.payment_succeeded_routimg_key)
    await queue.consume(handle_payment_events)