from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import Character, CharacterMastery, CharacterStat
from app.game.mastery import MasteryPath

STAT_NAMES = ("strength", "agility", "intelligence", "constitution", "willpower", "charisma")


async def ensure_progression_rows(session: AsyncSession, character: Character) -> None:
    stat = (await session.execute(select(CharacterStat).where(CharacterStat.character_id == character.id))).scalar_one_or_none()
    if stat is None:
        session.add(CharacterStat(character_id=character.id))
    for path in MasteryPath:
        existing = (await session.execute(select(CharacterMastery).where(CharacterMastery.character_id == character.id, CharacterMastery.path == path.value))).scalar_one_or_none()
        if existing is None:
            session.add(CharacterMastery(character_id=character.id, path=path.value))
    await session.flush()


async def spend_stat_point(session: AsyncSession, character: Character, stat_name: str) -> bool:
    if stat_name not in STAT_NAMES:
        return False
    stat = (await session.execute(select(CharacterStat).where(CharacterStat.character_id == character.id))).scalar_one_or_none()
    if stat is None or stat.available_points <= 0:
        return False
    setattr(stat, stat_name, getattr(stat, stat_name) + 1)
    stat.available_points -= 1
    await session.commit()
    return True
