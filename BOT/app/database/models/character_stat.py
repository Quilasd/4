from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import Base


class CharacterStat(Base):
    __tablename__ = "character_stats"
    __table_args__ = (UniqueConstraint("character_id", name="uq_character_stats_character"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    character_id: Mapped[int] = mapped_column(ForeignKey("characters.id", ondelete="CASCADE"), nullable=False, index=True)
    strength: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    agility: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    intelligence: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    constitution: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    willpower: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    charisma: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    available_points: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
