from typing import AsyncGenerator
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from config import settings

Base = declarative_base()
metadata = MetaData()

engine = create_async_engine(
    settings.DATABASE_URL, poolclass=NullPool, echo=settings.DEBUG
)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Provide a SQLAlchemy asynchronous session generator.

    This generator provides an asynchronous session that can be used for
    database operations. The session is automatically closed after use.

    Yields:
        AsyncSession: An asynchronous database session.
    """
    async with async_session_maker() as session:
        yield session
