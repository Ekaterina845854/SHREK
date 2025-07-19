from app.src.database import AsyncDbSession
from app.src.dependency.schemas import Task
from fastapi import APIRouter

from . import service

app = APIRouter(
    prefix="/tasks",
)


@app.get("/{task_id}")
async def get_task(session: AsyncDbSession, task_id: str) -> Task:
    task = await service.get_task(session=session, task_id=task_id)
    return task