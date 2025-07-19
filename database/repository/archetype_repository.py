from sqlalchemy.ext.asyncio import AsyncSession

from app.src.database.models import Archetype

from .repository import BaseRepository


class ArchetypeRepository(BaseRepository[Archetype]):
    model = Archetype