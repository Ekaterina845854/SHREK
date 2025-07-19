from contextlib import asynccontextmanager
from typing import Annotated

from app.config import config
from fastapi import Depends
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine(
    config.SQLALCHEMY_DATABASE_URL
)

SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    
    def dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


async def get_db():
    async with SessionLocal() as session:
        async with session.begin():
            yield session


@asynccontextmanager
async def m_get_db():
    async with SessionLocal() as session:
        async with session.begin():
            yield session


AsyncDbSession = Annotated[AsyncSession, Depends(get_db)]
