from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy import select

from app.bot.keyboards.main import back_menu, main_menu
from app.database.models import Character, World
from app.database.session import SessionFactory
from app.game.mastery import MASTERY_PATHS
from app.services.character import get_character

router = Router(name="game")


async def render_main(message: Message) -> None:
    await message.answer("🏰 Главное меню", reply_markup=main_menu())


@router.message(Command("menu"))
async def menu(message: Message, state: FSMContext) -> None:
    await state.clear()
    async with SessionFactory() as session:
        character = await get_character(session, message.from_user.id)
    if character is None:
        await message.answer("У вас пока нет персонажа. Используйте /start.")
        return
    await render_main(message)


@router.callback_query(F.data == "menu:main")
async def menu_main(callback: CallbackQuery) -> None:
    await callback.message.edit_text("🏰 Главное меню", reply_markup=main_menu())
    await callback.answer()


@router.callback_query(F.data == "menu:profile")
async def profile(callback: CallbackQuery) -> None:
    async with SessionFactory() as session:
        character = await get_character(session, callback.from_user.id)
        if character is None:
            await callback.answer("Персонаж не найден.", show_alert=True)
            return
        world = await session.get(World, character.world_id)
    gender = "Мужской" if character.gender == "male" else "Женский"
    text = (
        f"👤 <b>{character.name}</b>\n\n"
        f"🌍 Мир: {world.name if world else '—'}\n"
        f"🗺️ Континент: {character.continent}\n"
        f"🧬 Раса: {character.race}\n"
        f"⚧ Пол: {gender}\n"
        f"🎂 Возраст: {character.age}\n"
        f"⭐ Уровень: {character.level}\n"
        f"✨ Опыт: {character.experience}\n"
        f"❤️ Статус: {character.status}"
    )
    await callback.message.edit_text(text, reply_markup=back_menu(), parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data == "menu:mastery")
async def mastery(callback: CallbackQuery) -> None:
    text = "⚔️ <b>Мастерство</b>\n\n"
    for path in MASTERY_PATHS.values():
        text += f"• {path.names[0]} → {path.names[-1]}\n"
    text += "\nУ персонажа нет жёсткого класса: направления развиваются независимо."
    await callback.message.edit_text(text, reply_markup=back_menu(), parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data == "menu:inventory")
async def inventory(callback: CallbackQuery) -> None:
    await callback.message.edit_text("🎒 <b>Инвентарь</b>\n\nПока пусто.", reply_markup=back_menu(), parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data == "menu:world")
async def world(callback: CallbackQuery) -> None:
    async with SessionFactory() as session:
        character = await get_character(session, callback.from_user.id)
        if character is None:
            await callback.answer("Персонаж не найден.", show_alert=True)
            return
        world = await session.get(World, character.world_id)
    await callback.message.edit_text(
        f"🗺️ <b>{world.name if world else 'Мир'}</b>\n\n"
        f"Статус: {world.status if world else '—'}\n"
        f"Текущая дата мира: {world.current_game_date if world else '—'}\n\n"
        "Карта мира будет вынесена в Mini App.",
        reply_markup=back_menu(),
        parse_mode="HTML",
    )
    await callback.answer()
