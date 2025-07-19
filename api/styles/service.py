from app.src.database.models import Style
from app.src.database.repository import StyleRepository
from app.src.dependency.exceptions import NotFoundError
from app.src.dependency.schemas import CreateStyle
from sqlalchemy.ext.asyncio import AsyncSession


async def get_all_styles(session: AsyncSession) -> Style:
    styles = await StyleRepository.find_all(session)
    
    return styles


async def get_style(session: AsyncSession, style_id: int) -> Style:
    style = await StyleRepository.find_one_or_none(session, style_id=style_id)
    
    if not style:
        raise NotFoundError()
    
    return style


async def create_style(session: AsyncSession, new_style: CreateStyle) -> Style:
    style = await StyleRepository.add(session, **new_style.model_dump())
    
    return style