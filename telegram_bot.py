import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telegram_auth.settings')
django.setup()

from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from django.conf import settings
from accounts.models import Profile



bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class RegisterForm(StatesGroup):
    first_name = State()
    last_name = State()
    password = State()


async def on_startup(*args):
    print("Bot it's the work")


@dp.message_handler(commands=["start"], state="*")
async def start_registration(message: types.Message):
    await message.answer("Вітаємо! Для реєстрації введіть своє ім'я:")
    await RegisterForm.first_name.set()


@dp.message_handler(state=RegisterForm.first_name)
async def process_first_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["first_name"] = message.text

    await message.answer("Введіть своє прізвище::")
    await RegisterForm.next()


@dp.message_handler(state=RegisterForm.last_name)
async def process_last_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["last_name"] = message.text

    await message.answer("Введіть свій пароль:")
    await RegisterForm.next()


@dp.message_handler(state=RegisterForm.password)
async def process_password(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["password"] = message.text

    user_data = {
        "telegram_id": message.chat.id,
        "first_name": data["first_name"],
        "last_name": data["last_name"],
        "username": message.from_user.username,
        "password": data["password"],
    }
    print(user_data)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
