from app.src.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from . import Archetype, Style


class Character(Base):
    __tablename__ = "characters"
    
    character_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    archetype_id: Mapped[int] = mapped_column(
        ForeignKey(Archetype.archetype_id)
    )
    style_id: Mapped[int] = mapped_column(
        ForeignKey(Style.style_id)
    )
    name: Mapped[str] = mapped_column()
    user_id: Mapped[int] = mapped_column(
        nullable=True, comment="telegram user id"
    )

    archetype: Mapped[Archetype] = relationship("Archetype")
    style: Mapped[Style] = relationship("Style")