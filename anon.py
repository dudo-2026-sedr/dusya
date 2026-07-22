import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.enums import ButtonStyle

API_TOKEN = "8816417120:AAFqCxA7PflaO5Jz2_QLtqd1M4Z1m-9ibm8"
ADMIN_ID = 5480751648

# ===== КАСТОМНЫЕ ЭМОДЗИ (вставь свои ID) =====
EMOJI_MAIN = "5886632311327299287"   # для приветствия
EMOJI_SEND = "5794158469988753026"   # для сообщения "Напиши в наш чат..."
EMOJI_BACK  = "5794064968550718961"  # для кнопки "Назад" (опционально)
# =============================================

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# --- КНОПКИ ---

main_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(
            text="Отправить сообщение",
            callback_data="send_message",
            style=ButtonStyle.SUCCESS  # зелёный цвет
        )]
    ]
)

back_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="⬅ Назад", callback_data="back_to_main")]
    ]
)

# --- ХЕНДЛЕРЫ ---

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    # Используем HTML-разметку, чтобы вставить кастомный эмодзи
    await message.answer(
        f'Привет, я создан @cdsai, <emoji id="{EMOJI_MAIN}">&#8291;</emoji> напиши что то, я передам!',
        parse_mode="HTML",
        reply_markup=main_kb
    )

@dp.callback_query(F.data == "send_message")
async def ask_for_message(callback: types.CallbackQuery):
    await callback.message.edit_text(
        f'Напиши в наш чат то что ты хочешь отправить @cdsai <emoji id="{EMOJI_SEND}">&#8291;</emoji>',
        parse_mode="HTML",
        reply_markup=back_kb
    )
    await callback.answer()

@dp.callback_query(F.data == "back_to_main")
async def back_to_main(callback: types.CallbackQuery):
    await callback.message.edit_text(
        f'Привет, я создан @cdsai, <emoji id="{EMOJI_MAIN}">&#8291;</emoji> напиши что то, я передам!',
        parse_mode="HTML",
        reply_markup=main_kb
    )
    await callback.answer()

@dp.message(F.text)
async def handle_message(message: types.Message):
    user = message.from_user
    user_id = user.id
    username = user.username or "нет username"
    full_name = user.full_name

    report = (
        f"📩 *Новое анонимное сообщение!*\n\n"
        f"👤 *От:* {full_name}\n"
        f"🆔 *ID:* `{user_id}`\n"
        f"🔖 *Username:* @{username}\n\n"
        f"💬 *Текст:*\n{message.text}"
    )

    try:
        await bot.send_message(ADMIN_ID, report, parse_mode="Markdown")
        await message.answer("✅ Сообщение отправлено!")
    except Exception as e:
        logging.error(f"Ошибка: {e}")
        await message.answer("❌ Произошла ошибка. Попробуй позже.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())