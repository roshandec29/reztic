from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from contextlib import asynccontextmanager
from .base import Base
from ..config import config


class DBConnection:
    def __init__(self):
        self._engine = create_async_engine(
            config.DB_URL,
            echo=False,
            pool_size=10,
            max_overflow=20,
            future=True,
        )
        self._sessionmaker = async_sessionmaker(
            self._engine, expire_on_commit=False, class_=AsyncSession
        )

    @asynccontextmanager
    async def get_session(self):
        async with self._sessionmaker() as session:
            yield session

    async def commit_and_close(self, session: AsyncSession):
        try:
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()

    async def dispose(self):
        await self._engine.dispose()


db_connection = DBConnection()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with db_connection.get_session() as session:
        yield session
