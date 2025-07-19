from app.src.database import AsyncDbSession
from app.src.dependency.schemas import Archetype, CreateArchetype
from fastapi import APIRouter

from . import service

app = APIRouter(
    prefix="/archetypes",
)


@app.get("")
async def get_all_archetypes(session: AsyncDbSession) -> list[Archetype]:
    archetypes = await service.get_all_archetypes(session=session)
    return archetypes


@app.get("/{archetype_id}")
async def get_archetype(session: AsyncDbSession, archetype_id: int) -> Archetype:
    archetype = await service.get_archetype(session=session, archetype_id=archetype_id)
    
    return archetype


@app.post("")
async def create_archetype(session: AsyncDbSession, archetype: CreateArchetype) -> Archetype:
    archetype = await service.create_archetype(session=session, new_archetype=archetype)
    
    return archetype