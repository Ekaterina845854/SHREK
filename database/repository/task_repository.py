from app.src.database.models import Task
from app.src.dependency.constants import TaskStatuses
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update

from .repository import BaseRepository


class TaskRepository(BaseRepository[Task]):
    model = Task
    
    @classmethod
    async def update_status_in_progress(cls, session: AsyncSession, task_id: str) -> None:
        await TaskRepository.update(session, task_id, status=TaskStatuses.IN_PROGRESS)
        
    @classmethod
    async def update_status_completed(cls, session: AsyncSession, task_id: str) -> None:
        await TaskRepository.update(session, task_id, status=TaskStatuses.COMPLETED)
    
    @classmethod
    async def update_status_failed(cls, session: AsyncSession, task_id: str) -> None:
        await TaskRepository.update(session, task_id, status=TaskStatuses.FAILED)