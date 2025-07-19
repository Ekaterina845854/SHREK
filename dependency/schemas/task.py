from typing import Optional

from pydantic import BaseModel


class BaseTask(BaseModel):
    task_id: str
    status: str
    result: Optional[str]
            
    class Config:
        from_attributes = True


class Task(BaseTask):
    pass
