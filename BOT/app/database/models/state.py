from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import Base


class CharacterResource(Base):
    __tablename__ = "character_resources"
    __table_args__ = (UniqueConstraint("character_id", name="uq_character_resources_character"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    character_id: Mapped[int] = mapped_column(ForeignKey("characters.id", ondelete="CASCADE"), nullable=False, index=True)
    health: Mapped[int] = mapped_column(Integer, default=100, nullable=False)
    max_health: Mapped[int] = mapped_column(Integer, default=100, nullable=False)
    stamina: Mapped[int] = mapped_column(Integer, default=100, nullable=False)
    max_stamina: Mapped[int] = mapped_column(Integer, default=100, nullable=False)
    mana: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    max_mana: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
