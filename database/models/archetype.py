from app.src.database import Base
from sqlalchemy.orm import Mapped, mapped_column


class Archetype(Base):
    __tablename__ = "archetypes"
    
    archetype_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    user_id: Mapped[int] = mapped_column(
        nullable=True, comment="telegram user id"
    )
