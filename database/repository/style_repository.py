from sqlalchemy.ext.asyncio import AsyncSession

from app.src.database.models import Style

from .repository import BaseRepository


class StyleRepository(BaseRepository[Style]):
    model = Style