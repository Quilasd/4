from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import Base


class CharacterEquipment(Base):
    __tablename__ = "character_equipment"
    __table_args__ = (UniqueConstraint("character_id", "slot", name="uq_character_equipment_slot"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    character_id: Mapped[int] = mapped_column(ForeignKey("characters.id", ondelete="CASCADE"), nullable=False, index=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id", ondelete="CASCADE"), nullable=False)
    slot: Mapped[str] = mapped_column(nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
