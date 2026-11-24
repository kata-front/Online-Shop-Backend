from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from .config import settings

engine = create_async_engine(
    url=settings.db_url
)
SessionLocal = async_sessionmaker(
    bind=engine, expire_on_commit=False
)

async def get_db():
    async with SessionLocal() as session:
        yield session