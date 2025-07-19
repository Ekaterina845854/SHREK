from app.src.database.models import Task
from app.src.database.repository import TaskRepository
from app.src.dependency.exceptions import NotFoundError
from sqlalchemy.ext.asyncio import AsyncSession


async def get_task(session: AsyncSession, task_id: str) -> Task:
    task = await TaskRepository.find_one_or_none(session, task_id=task_id)
    
    if not task:
        raise NotFoundError()
    
    return task