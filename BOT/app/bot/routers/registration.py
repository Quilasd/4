from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.bot.keyboards.registration import continent_menu, gender_menu, race_menu, world_menu
from app.bot.states.registration import RegistrationStates
from app.database.models import World
from app.database.session import SessionFactory
from app.services.registration import create_character, get_active_worlds, get_or_create_user

router = Router(name="registration")

CONTINENTS = [
    ("continent_1", "🌍 Континент I"),
    ("continent_2", "🌎 Континент II"),
    ("continent_3", "🌏 Континент III"),
]

RACES = [
    ("human", "🧑 Люди"),
    ("elf", "🧝 Эльфы"),
    ("half_elf", "🧝‍♂️ Полуэльфы"),
    ("dwarf", "⛏️ Дворфы"),
]


@router.message(CommandStart())
async def start(message: Message, state: FSMContext) -> None:
    async with SessionFactory() as session:
        await get_or_create_user(session, message.from_user.id, message.from_user.username)
        await session.commit()
        worlds = await get_active_worlds(session)
    if not worlds:
        await message.answer("🌍 Активных миров пока нет. Ожидайте создания мира администрацией.")
        return
    await state.set_state(RegistrationStates.choosing_world)
    await message.answer("🌍 Добро пожаловать.\n\nВыберите мир:", reply_markup=world_menu([(w.id, w.name) for w in worlds]))


@router.callback_query(RegistrationStates.choosing_world, F.data.startswith("world:"))
async def choose_world(callback: CallbackQuery, state: FSMContext) -> None:
    value = callback.data.split(":", 1)[1]
    if value == "create":
        await callback.answer("Создание мира пока доступно только администрации.")
        return
    try:
        world_id = int(value)
    except ValueError:
        await callback.answer("Некорректный мир.", show_alert=True)
        return
    async with SessionFactory() as session:
        world = await session.get(World, world_id)
        if world is None or world.status != "active":
            await callback.answer("Мир больше недоступен.", show_alert=True)
            return
    await state.update_data(world_id=world_id)
    await state.set_state(RegistrationStates.choosing_continent)
    await callback.message.edit_text("🗺️ Выберите континент, на котором родился ваш персонаж:", reply_markup=continent_menu(CONTINENTS))
    await callback.answer()


@router.callback_query(RegistrationStates.choosing_continent, F.data.startswith("continent:"))
async def choose_continent(callback: CallbackQuery, state: FSMContext) -> None:
    continent = callback.data.split(":", 1)[1]
    if continent not in {key for key, _ in CONTINENTS}:
        await callback.answer("Некорректный континент.", show_alert=True)
        return
    await state.update_data(continent=continent)
    await state.set_state(RegistrationStates.choosing_name)
    await callback.message.edit_text("🧙 Введите имя персонажа:")
    await callback.answer()


@router.message(RegistrationStates.choosing_name)
async def choose_name(message: Message, state: FSMContext) -> None:
    name = message.text.strip() if message.text else ""
    if not 2 <= len(name) <= 32:
        await message.answer("Имя должно содержать от 2 до 32 символов.")
        return
    await state.update_data(name=name)
    await state.set_state(RegistrationStates.choosing_gender)
    await message.answer("Выберите пол:", reply_markup=gender_menu())


@router.callback_query(RegistrationStates.choosing_gender, F.data.startswith("gender:"))
async def choose_gender(callback: CallbackQuery, state: FSMContext) -> None:
    gender = callback.data.split(":", 1)[1]
    if gender not in {"male", "female"}:
        await callback.answer("Некорректный вариант.", show_alert=True)
        return
    await state.update_data(gender=gender)
    await state.set_state(RegistrationStates.choosing_race)
    await callback.message.edit_text("🧬 Выберите расу:", reply_markup=race_menu(RACES))
    await callback.answer()


@router.callback_query(RegistrationStates.choosing_race, F.data.startswith("race:"))
async def choose_race(callback: CallbackQuery, state: FSMContext) -> None:
    race = callback.data.split(":", 1)[1]
    if race not in {key for key, _ in RACES}:
        await callback.answer("Некорректная раса.", show_alert=True)
        return
    data = await state.get_data()
    async with SessionFactory() as session:
        user = await get_or_create_user(session, callback.from_user.id, callback.from_user.username)
        world = await session.get(World, data["world_id"])
        if world is None or world.status != "active":
            await callback.answer("Мир больше недоступен.", show_alert=True)
            return
        character = await create_character(session, user, world, data["name"], data["gender"], race, data["continent"])
    await state.clear()
    await callback.message.edit_text(f"✅ Персонаж создан!\n\n👤 {character.name}\n🧬 {character.race}\n🗺️ {character.continent}\n⚔️ Уровень: {character.level}\n\nДобро пожаловать в мир.")
    await callback.answer()
