import asyncio
import logging
from html import escape

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


API_TOKEN = "8816417120:AAFqCxA7PflaO5Jz2_QLtqd1M4Z1m-9ibm8"
ADMIN_ID = 5480751648

# Вставь ID своих кастомных эмодзи
EMOJI_MAIN = "5794064968550718961"
EMOJI_SEND = "5886632311327299287"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


# --- КНОПКИ ---

main_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Отправить сообщение",
                callback_data="send_message",
            )
        ]
    ]
)

back_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="⬅ Назад",
                callback_data="back_to_main",
            )
        ]
    ]
)


# --- ХЕНДЛЕРЫ ---

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    text = (
        f'Привет, я создан @cdsai '
        f'<tg-emoji emoji-id="{EMOJI_MAIN}">🤖</tg-emoji> '
        f'Напиши что-то, я передам!'
    )

    await message.answer(
        text,
        parse_mode="HTML",
        reply_markup=main_kb,
    )


@dp.callback_query(F.data == "send_message")
async def ask_for_message(callback: types.CallbackQuery):
    text = (
        f'Напиши в наш чат то, что хочешь отправить @cdsai '
        f'<tg-emoji emoji-id="{EMOJI_SEND}">✉️</tg-emoji>'
    )

    if callback.message:
        await callback.message.edit_text(
            text,
            parse_mode="HTML",
            reply_markup=back_kb,
        )

    await callback.answer()


@dp.callback_query(F.data == "back_to_main")
async def back_to_main(callback: types.CallbackQuery):
    text = (
        f'Привет, я создан @cdsai '
        f'<tg-emoji emoji-id="{EMOJI_MAIN}">🤖</tg-emoji> '
        f'Напиши что-то, я передам!'
    )

    if callback.message:
        await callback.message.edit_text(
            text,
            parse_mode="HTML",
            reply_markup=main_kb,
        )

    await callback.answer()


@dp.message(F.text)
async def handle_message(message: types.Message):
    user = message.from_user

    if user is None or message.text is None:
        return

    username = f"@{escape(user.username)}" if user.username else "отсутствует"

    report = (
        "<b>📩 Новое анонимное сообщение!</b>\n\n"
        f"<b>👤 От:</b> {escape(user.full_name)}\n"
        f"<b>🆔 ID:</b> <code>{user.id}</code>\n"
        f"<b>🔖 Username:</b> {username}\n\n"
        f"<b>💬 Текст:</b>\n{escape(message.text)}"
    )

    try:
        await bot.send_message(
            ADMIN_ID,
            report,
            parse_mode="HTML",
        )
        await message.answer("✅ Сообщение отправлено!")

    except Exception:
        logging.exception("Ошибка при отправке сообщения")
        await message.answer("❌ Произошла ошибка. Попробуй позже.")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
    
