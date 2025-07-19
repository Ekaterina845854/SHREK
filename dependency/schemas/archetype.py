from typing import Optional

from pydantic import BaseModel


class BaseArchetype(BaseModel):
    name: str
    user_id: Optional[int] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True
        extra = "allow"


class Archetype(BaseArchetype):
    archetype_id: int


class CreateArchetype(BaseArchetype):
    pass
