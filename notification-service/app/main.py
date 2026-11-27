from contextlib import asynccontextmanager
from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .config import settings
from .schemas import NotifReadSchema
from .database import engine, get_db
from .models import Base, NotifORM
from .rabbitmq import connect_rabbitmq, start_payments_consume

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    connection = await connect_rabbitmq(settings.rebbitmq_url)
    await start_payments_consume(connection)

    yield

    await engine.dispose()

app = FastAPI(lifespan=lifespan)

@app.get('/notifications', response_model=list[NotifReadSchema])
async def get_notifs(
    db: AsyncSession = Depends(get_db)
):
    notifs = (await db.scalars(
        select(NotifORM)
    )).all()
    return [NotifReadSchema.model_validate(item) for item in notifs]

@app.get('/notifications/{id}', response_model=NotifReadSchema)
async def get_notif(
    id: UUID,
    db: AsyncSession = Depends(get_db)
):
    notif = await db.get(NotifORM, id)

    if notif is None:
        raise HTTPException(status_code=404, detail="Notification not found")

    return NotifReadSchema.model_validate(notif)
    