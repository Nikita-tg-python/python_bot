import asyncio
import os
import database
from aiohttp import web
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message, FSInputFile


async def log_action(message, action_text: str):
    await database.log_user_action(
        user_id=message.from_user.id,
        first_name=message.from_user.first_name,
        username=message.from_user.username,
        action=action_text,
    )


load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("Переменная BOT_TOKEN не найдена!")

dp = Dispatcher()

router = Router()
my_reply_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="👤 Моє резюме"),
            KeyboardButton(text="👨‍💻 Посилання на мій gitHub"),
        ],
        [KeyboardButton(text="📞 Звязок зі мною")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Обери дію",
)


async def health_check(request):
    return web.Response(text="Bot is alive!")


@dp.message(Command("start"))
async def cmd_start(message: types.Message):

    await message.answer("Доброго дня вас вітає резюме бот", reply_markup=my_reply_kb)

    await log_action(message, "Запустил бота (/start)")


@dp.message(F.text == "👤 Моє резюме")
async def show_profile(message: types.Message):

    resume_file = FSInputFile("Ризюме.pdf")

    await message.answer_document(
        document=resume_file, caption="Доброго дня! Ось моє резюме📄"
    )

    await log_action(message, "Резюме")


@dp.message(F.text == "👨‍💻 Посилання на мій gitHub")
async def show_profile(message: types.Message):

    await message.answer("https://github.com/Nikita-tg-python")

    await log_action(message, "Гит хаб")


@dp.message(F.text == "📞 Звязок зі мною")
async def show_profile(message: types.Message):

    await message.answer(
        "Номер телефона: +380 68 192 65 18\nТелеграм: @Necro_fus\nПочта: nikitakryvyj@gmail.com"
    )
    await log_action(message, "Номер")


@dp.message()
async def echo_message(message: types.Message):

    await message.reply("Виберіть дію")

    await log_action(message, "Неправильна дія  ")


async def main():

    await database.create_pool()
    await database.create_table()

    bot = Bot(token=TOKEN)

    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
