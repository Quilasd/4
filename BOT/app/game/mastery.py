from dataclasses import dataclass


@dataclass(frozen=True)
class MasteryPath:
    key: str
    names: tuple[str, ...]


MASTERY_PATHS = {
    "sword": MasteryPath("sword", ("Новичок", "Воин", "Опытный воин", "Мастер", "Великий мастер", "Мастер клинка", "Легендарный мечник")),
    "archery": MasteryPath("archery", ("Новичок", "Лучник", "Опытный лучник", "Мастер", "Великий мастер", "Мастер стрельбы", "Легендарный стрелок")),
    "spear": MasteryPath("spear", ("Новичок", "Копейщик", "Опытный копейщик", "Мастер", "Великий мастер", "Мастер копья", "Легендарный копейщик")),
    "cavalry": MasteryPath("cavalry", ("Новичок", "Всадник", "Опытный всадник", "Мастер кавалерии", "Великий всадник", "Рыцарь", "Легендарный рыцарь")),
    "magic": MasteryPath("magic", ("Ученик", "Маг", "Высший маг", "Великий маг", "Архимаг", "Верховный маг")),
}


def rank_for(path: str, mastery_level: int) -> str:
    ranks = MASTERY_PATHS[path].names
    index = max(0, min(mastery_level, len(ranks) - 1))
    return ranks[index]
