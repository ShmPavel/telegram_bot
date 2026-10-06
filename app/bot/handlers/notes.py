from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.keyboards import main_menu
from app.bot.states import NoteStates
from app.repositories.notes import create_note, get_last_notes
from app.repositories.users import get_or_create_user

router = Router()


@router.callback_query(F.data == "menu:save")
async def on_save(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(NoteStates.waiting_for_text)
    await callback.message.edit_text("Отправь текст, который нужно сохранить.")
    await callback.answer()


@router.message(NoteStates.waiting_for_text, F.text)
async def on_text(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
) -> None:
    user = await get_or_create_user(session, message.from_user.id, message.from_user.username)
    await create_note(session, user.id, message.text)
    await session.commit()

    await state.clear()
    await message.answer("Сохранено.", reply_markup=main_menu())


@router.callback_query(F.data == "menu:list")
async def on_list(callback: CallbackQuery, session: AsyncSession) -> None:
    user = await get_or_create_user(session, callback.from_user.id, callback.from_user.username)
    notes = await get_last_notes(session, user.id, limit=10)

    if not notes:
        await callback.message.edit_text(
            "Пока ничего не записано.",
            reply_markup=main_menu(),
        )
        await callback.answer()
        return

    lines = []
    for n in notes:
        ts = n.created_at.strftime("%d.%m %H:%M")
        lines.append(f"• [{ts}] {n.text}")

    await callback.message.edit_text(
        "Последние записи:\n\n" + "\n".join(lines),
        reply_markup=main_menu(),
    )
    await callback.answer()