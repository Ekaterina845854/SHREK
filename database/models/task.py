from datetime import datetime

from app.src.database import Base
from sqlalchemy import DateTime, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.src.dependency.constants import TaskStatuses


class Task(Base):
    __tablename__ = "tasks"
    
    task_id: Mapped[str] = mapped_column(primary_key=True, nullable=False)
    status: Mapped[str] = mapped_column(nullable=False, default=TaskStatuses.PENDING)
    params: Mapped[dict] = mapped_column(JSONB, nullable=False)
    result: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False), server_default=func.now(), onupdate=func.now()
    )