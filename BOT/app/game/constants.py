from enum import StrEnum


class Gender(StrEnum):
    MALE = "male"
    FEMALE = "female"


class Race(StrEnum):
    HUMAN = "human"
    ELF = "elf"
    HALF_ELF = "half_elf"
    DWARF = "dwarf"


class CharacterStatus(StrEnum):
    ALIVE = "alive"
    DEAD = "dead"


class ItemSlot(StrEnum):
    HEAD = "head"
    BODY = "body"
    LEGS = "legs"
    HANDS = "hands"
    FEET = "feet"
    MAIN_HAND = "main_hand"
    OFF_HAND = "off_hand"
    ACCESSORY = "accessory"


STARTING_LEVEL = 1
STARTING_EXPERIENCE = 0
STARTING_AGE = 18
