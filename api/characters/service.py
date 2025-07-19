from typing import Optional
import uuid
from app.src.database.models import Character
from app.src.database.repository import CharacterRepository, TaskRepository
from app.src.dependency import schemas
from app.src.dependency.exceptions import NotFoundError, NoPermissionsError
from app.src.dependency.schemas import CreateCharacter
from app.src.queue import tasks
from sqlalchemy.ext.asyncio import AsyncSession


async def expand_character(character: Character, expand: list[str]) -> schemas.Character:
    return schemas.Character(
        character_id=character.character_id,
        name=character.name,
        user_id=character.user_id,
        archetype_id=character.archetype_id,
        style_id=character.style_id,
        archetype=character.archetype if "archetype" in expand else None,
        style=character.style if "style" in expand else None,
    )


async def get_all_characters(
    session: AsyncSession,
    expand: list[str],
    user_id: Optional[int] = None,
    only: Optional[bool] = None,
) -> list[Character]:
    characters = []
    if user_id:
        print(user_id)
        
        user_characters = await CharacterRepository.find_all(session, user_id=user_id)
        characters.extend(user_characters)
        
        if only:
            return [await expand_character(character, expand=expand) for character in characters]
    
    base_characters = await CharacterRepository.find_all(session, user_id=None)
    characters.extend(base_characters)
    
    return [await expand_character(character, expand=expand) for character in characters]


async def get_character(
    session: AsyncSession, character_id: int, expand: list[str], user_id: Optional[int]=None
) -> Character:
    character = await CharacterRepository.find_one_or_none(
        session, character_id=character_id
    )

    if not character or (character.user_id is not None and character.user_id != user_id):
        raise NotFoundError()
    
    return await  expand_character(character, expand=expand)


async def create_character(session: AsyncSession, new_character: CreateCharacter, expand: list[str]) -> Character:
    character = await CharacterRepository.add(session, **new_character.model_dump())
    
    return await expand_character(character, expand=expand)


async def character_speech(
    session: AsyncSession, character_id: int, query: str, user_id: int
) -> dict[str, str]:
    character = await CharacterRepository.find_one_or_none(
        session, character_id=character_id
    )
    
    if not character or (character.user_id is not None and character.user_id != user_id):
        raise NotFoundError
    
    task_id = str(uuid.uuid4())
    params={
        "character_id": character_id,
        "style_id": character.style_id,
        "archetype_id": character.archetype_id,
        "query": query,
        "user_id": user_id,
    }
    
    job = tasks.generate_character_response.send(character.character_id, query="test", task_id=task_id, params=params)
    
    await TaskRepository.add(
        session, task_id=task_id, params=params
    )
    
    return {
        "response": task_id
    }


async def delete_character(session: AsyncSession, character_id: int, user_id: int) -> None:
    character = await CharacterRepository.find_one_or_none(session, character_id=character_id)
    
    if not character or (character.user_id is not None and character.user_id != user_id):
        raise NotFoundError()
    
    if character.user_id != user_id:
        raise NoPermissionsError()
    
    await CharacterRepository.delete(session, id=character_id)