from typing import Optional

from pydantic import BaseModel


class BaseStyle(BaseModel):
    name: str
    user_id: Optional[int] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True
        extra = "allow"


class Style(BaseStyle):
    style_id: int


class CreateStyle(BaseStyle):
    pass
