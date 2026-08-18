from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WorldContext:
    world_id: int
    user_id: int
    role: str = "player"
