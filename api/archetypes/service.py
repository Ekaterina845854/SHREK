from app.src.database.models import Archetype
from app.src.database.repository import ArchetypeRepository
from app.src.dependency.exceptions import NotFoundError
from app.src.dependency.schemas import CreateArchetype
from sqlalchemy.ext.asyncio import AsyncSession


async def get_all_archetypes(session: AsyncSession) -> Archetype:
    archetypes = await ArchetypeRepository.find_all(session)
    
    return archetypes


async def get_archetype(session: AsyncSession, archetype_id: int) -> Archetype:
    archetype = await ArchetypeRepository.find_one_or_none(session, archetype_id=archetype_id)
    
    if not archetype:
        raise NotFoundError()
    
    return archetype


async def create_archetype(session: AsyncSession, new_archetype: CreateArchetype) -> Archetype:
    archetype = await ArchetypeRepository.add(session, **new_archetype.model_dump())
    
    return archetype