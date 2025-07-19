from typing import Optional

from pydantic import BaseModel

from .archetype import Archetype
from .style import Style


class BaseCharacter(BaseModel):
    name: str
    user_id: Optional[int] = None
    archetype_id: int
    style_id: int

    class Config:
        from_attributes = True


class Character(BaseCharacter):
    character_id: int
    archetype: Optional[Archetype] = None
    style: Optional[Style] = None


class CreateCharacter(BaseCharacter):
    pass
