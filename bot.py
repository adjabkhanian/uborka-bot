import asyncio
from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.markdown import hbold
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

API_TOKEN = "7865773975:AAFG4fNceKdcbfiOxs4ogDcew6Hsj2Wkxu0"
CHAT_ID = -1002472216382  # Заменить на ID твоей группы

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())
scheduler = AsyncIOScheduler()

# Группы уборки
groups = [
    "1–5", "6–10", "11–15", "16–20", "21–25", "26–29 + PS1", "30–34", "35–38 + PS2"
]

# Храним индекс текущей группы
current_group_index = 0


# Генерация клавиатуры
def get_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="✅ Убрано", callback_data="done")]]
    )


# Отправка задания на уборку
# Отправка задания на уборку
async def send_task():
    global current_group_index
    group = groups[current_group_index]
    now = datetime.now().strftime("%d.%m.%Y %H:%M")

    text = f"🧽 <b>Задание на уборку</b>\n\n" \
           f"{hbold('Время')}: {now}\n" \
           f"{hbold('Убрать ПК')}: {group}\n\n" \
           f"После уборки нажмите кнопку ⬇️"

    await bot.send_message(
        chat_id=CHAT_ID,
        message_thread_id=3146,  # 👉 это ID топика "uborka"
        text=text,
        reply_markup=get_keyboard()
    )

    # Переход к следующей группе
    current_group_index = (current_group_index + 1) % len(groups)


# Ответ на кнопку "Убрано"
@dp.callback_query(F.data == "done")
async def cleaned(callback: types.CallbackQuery):
    user = callback.from_user
    username = user.full_name

    new_text = callback.message.text + f"\n\n✅ Уборка выполнена: <b>{username}</b>"

    await callback.message.edit_text(new_text)
    await callback.answer("Отметка сохранена!")


# Команда /segodnya — показывает текущую группу
@dp.message(F.text.startswith("/segodnya"))
async def cmd_today(message: types.Message):
    prev_index = (current_group_index - 1) % len(groups)
    await message.answer(f"🧽 Сегодня убирается: <b>{groups[prev_index]}</b>")


# Планировщик
def schedule_jobs():
    # В 10:00
    scheduler.add_job(send_task, trigger="cron", hour=22, minute=26)
    # В 22:00
    scheduler.add_job(send_task, trigger="cron", hour=22, minute=27)


async def main():
    schedule_jobs()
    scheduler.start()

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())