from aiogram.fsm.state import State, StatesGroup


class RegistrationStates(StatesGroup):
    choosing_world = State()
    choosing_continent = State()
    choosing_name = State()
    choosing_gender = State()
    choosing_race = State()
