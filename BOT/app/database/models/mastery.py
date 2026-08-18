from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import Base


class CharacterMastery(Base):
    __tablename__ = "character_masteries"
    __table_args__ = (UniqueConstraint("character_id", "path", name="uq_character_mastery_path"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    character_id: Mapped[int] = mapped_column(ForeignKey("characters.id", ondelete="CASCADE"), nullable=False, index=True)
    path: Mapped[str] = mapped_column(String(32), nullable=False)
    level: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    experience: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
