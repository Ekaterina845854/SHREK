from app.src.database.models import Character
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .repository import BaseRepository


class CharacterRepository(BaseRepository[Character]):
    model = Character
    
    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, **filter) -> Character:
        query = (
            select(cls.model)
            .filter_by(**filter)
            .options(selectinload(cls.model.archetype), selectinload(cls.model.style))
            .limit(1)
        )
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, session: AsyncSession, **filter) -> list[Character]:
        query = (
            select(cls.model)
            .options(selectinload(cls.model.archetype), selectinload(cls.model.style))
        ).filter_by(**filter)
        
        result = await session.execute(query)
        return result.scalars().all()
    
    @classmethod
    async def add(cls, session: AsyncSession, **data) -> Character:
        new_item = cls.model(**data)
        session.add(new_item)
        
        await session.flush()
        await session.refresh(new_item, attribute_names=["archetype", "style"])
        
        return new_item