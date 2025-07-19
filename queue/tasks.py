import asyncio

import dramatiq
from app.src.database.core import m_get_db
from app.src.database.repository import TaskRepository, CharacterRepository

from .worker import redis_broker
from app.src.ai.service import model


@dramatiq.actor
def generate_character_response(character_id: int, query: str, task_id: str, params: dict):
    async def _inner():
        try:
            async with m_get_db() as session:
                await TaskRepository.update_status_in_progress(session, task_id)

                character = await CharacterRepository.find_one_or_none(session, character_id=character_id)
            
            # Имитация долгой обработки
            result = await asyncio.to_thread(
                model.generate_response, query, character.archetype.name, character.style.name
            )

            async with m_get_db() as session:
                await TaskRepository.update_status_completed(session, task_id)
                await TaskRepository.update(session, task_id, result=result)

        except Exception as e:
            async with m_get_db() as session:
                await TaskRepository.update_status_failed(session, task_id)
                await TaskRepository.update(session, task_id, result=str(e))

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    if loop.is_running():
        loop.create_task(_inner())
    else:
        loop.run_until_complete(_inner())