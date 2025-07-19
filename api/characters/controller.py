from typing import Optional

from app.src.database import AsyncDbSession
from app.src.dependency.schemas import Character, CreateCharacter
from fastapi import APIRouter, Depends, Query, status

from . import service

app = APIRouter(
    prefix="/characters",
)

def get_expand_fields(expand: str = Query("", description="Fields to expand, comma separated")) -> list[str]:
    return [field.strip() for field in expand.split(",") if field.strip()]


@app.get("")
async def get_all_characters(
    session: AsyncDbSession,
    user_id: Optional[int] = None,
    expand: list[str] = Depends(get_expand_fields),
    only: Optional[bool] = False,
) -> list[Character]:
    characters = await service.get_all_characters(session=session, expand=expand, user_id=user_id, only=only)
    return characters


@app.get("/{character_id}")
async def get_character(
    session: AsyncDbSession,
    character_id: int,
    user_id: Optional[int] = None,
    expand: list[str] = Depends(get_expand_fields)
) -> Character:
    character = await service.get_character(
        session=session, character_id=character_id, expand=expand, user_id=user_id
    )
    
    return character


@app.post("", status_code=status.HTTP_201_CREATED)
async def create_character(
    session: AsyncDbSession,
    character: CreateCharacter,
    expand: list[str] = Depends(get_expand_fields)
) -> Character:
    character = await service.create_character(session=session, new_character=character, expand=expand)
    
    return character


@app.post("/{character_id}")
async def character_speech(
    session: AsyncDbSession,
    character_id: int,
    user_id: int,
    query: str
) -> dict[str, str]:
    result = await service.character_speech(
        session=session, character_id=character_id, query=query, user_id=user_id
    )
    
    return result


@app.delete("/{character_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_character(session: AsyncDbSession, character_id: int, user_id: int) -> None:
    await service.delete_character(
        session=session, character_id=character_id, user_id=user_id
    )
