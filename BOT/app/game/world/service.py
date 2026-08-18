from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models.world import World
from app.database.models.world_member import WorldMember


async def create_world(session: AsyncSession, name: str, seed: str | None = None) -> World:
    world = World(name=name, seed=seed, current_game_date=datetime.now(timezone.utc))
    session.add(world)
    await session.flush()
    return world


async def add_member(session: AsyncSession, world_id: int, user_id: int, role: str = "player") -> WorldMember:
    member = WorldMember(world_id=world_id, user_id=user_id, role=role)
    session.add(member)
    await session.flush()
    return member


async def get_world(session: AsyncSession, world_id: int) -> World | None:
    result = await session.execute(select(World).where(World.id == world_id))
    return result.scalar_one_or_none()
