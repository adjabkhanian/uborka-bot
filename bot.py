import asyncio
from datetime import datetime
from pytz import timezone

from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.markdown import hbold
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# === НАСТРОЙКИ ===
API_TOKEN = "7865773975:AAFG4fNceKdcbfiOxs4ogDcew6Hsj2Wkxu0"
CHAT_ID = -1002472216382          # ID группы
THREAD_ID = 3146                  # ID топика ("уборка")

# === ИНИЦИАЛИЗАЦИЯ ===
bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())
scheduler = AsyncIOScheduler()

# === СПИСОК ГРУПП ===
groups = [
    "1–5", "6–10", "11–15", "16–20",
    "21–25", "26–29 + PS1", "30–34", "35–38 + PS2"
]
current_group_index = 0

# === КНОПКА "Убрано" ===
def get_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Убрано", callback_data="done")]
        ]
    )

# === ЗАДАНИЕ НА УБОРКУ ===
async def send_task():
    global current_group_index
    group = groups[current_group_index]
    now = datetime.now(timezone("Europe/Moscow")).strftime("%d.%m.%Y %H:%M")

    text = (
        "🧽 <b>Задание на уборку</b>\n\n"
        f"{hbold('Время')}: {now}\n"
        f"{hbold('Убрать ПК')}: {group}\n\n"
        "После уборки нажмите кнопку ⬇️"
    )

    try:
        await bot.send_message(
            chat_id=CHAT_ID,
            message_thread_id=THREAD_ID,
            text=text,
            reply_markup=get_keyboard()
        )
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")

    current_group_index = (current_group_index + 1) % len(groups)

# === ОБРАБОТКА КНОПКИ ===
@dp.callback_query(F.data == "done")
async def cleaned(callback: types.CallbackQuery):
    user = callback.from_user
    username = user.full_name

    new_text = callback.message.text + f"\n\n✅ Уборка выполнена: <b>{username}</b>"
    await callback.message.edit_text(new_text)
    await callback.answer("Отметка сохранена!")

# === КОМАНДА /segodnya ===
@dp.message(F.text.startswith("/segodnya"))
async def cmd_today(message: types.Message):
    prev_index = (current_group_index - 1) % len(groups)
    await message.answer(f"🧽 Сегодня убирается: <b>{groups[prev_index]}</b>")

# === РАСПИСАНИЕ ===
def schedule_jobs():
    tz = timezone("Europe/Moscow")
    scheduler.add_job(send_task, trigger="cron", hour=3, minute=35, timezone=tz)
    scheduler.add_job(send_task, trigger="cron", hour=3, minute=38, timezone=tz)

# === ЗАПУСК ===
async def main():
    schedule_jobs()
    scheduler.start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())