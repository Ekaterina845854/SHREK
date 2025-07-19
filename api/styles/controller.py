from app.src.database import AsyncDbSession
from app.src.dependency.schemas import Style, CreateStyle
from fastapi import APIRouter

from . import service

app = APIRouter(
    prefix="/styles",
)


@app.get("")
async def get_all_styles(session: AsyncDbSession) -> list[Style]:
    styles = await service.get_all_styles(session=session)
    return styles


@app.get("/{style_id}")
async def get_style(session: AsyncDbSession, style_id: int) -> Style:
    style = await service.get_style(session=session, style_id=style_id)
    
    return style


@app.post("")
async def create_style(session: AsyncDbSession, style: CreateStyle) -> Style:
    style = await service.create_style(session=session, new_style=style)
    
    return style