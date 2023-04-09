import os

import django
from aiogram.types.base import InputFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telegram_auth.settings')
django.setup()

from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from django.conf import settings
from accounts.models import Profile
from asgiref.sync import sync_to_async

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class RegisterForm(StatesGroup):
    first_name = State()
    last_name = State()
    password = State()


async def on_startup(*args):
    print("Bot it's the work")


async def check_user_exists(username: int) -> bool:
    try:
        user = await sync_to_async(Profile.objects.get)(username=username)
        return True
    except Profile.DoesNotExist:
        return False


@dp.message_handler(commands=["start"], state="*")
async def start_registration(message: types.Message):
    if await check_user_exists(message.from_user.username):
        await bot.send_message(
            message.from_user.id,
            f'Ви вже зареєстровані'
        )
    else:
        await message.answer("Вітаємо! Для реєстрації введіть своє ім'я:")
        await RegisterForm.first_name.set()


@dp.message_handler(state=RegisterForm.first_name)
async def process_first_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["first_name"] = message.text

    await message.answer("Введіть своє прізвище::")
    await RegisterForm.next()


async def get_profile_photo(chat_id: int) -> InputFile:
    profile_pictures = await dp.bot.get_user_profile_photos(chat_id)
    photo_path = f"static/photo/{chat_id}.jpg"
    if profile_pictures.total_count != 0:
        await profile_pictures.photos[0][-1].download(destination_file=photo_path)
        return photo_path


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

    create_user_sync = sync_to_async(Profile.objects.create_user)
    user = await create_user_sync(
        telegram_id=message.chat.id,
        first_name=data["first_name"],
        last_name=data["last_name"],
        password=data["password"],
        username=message.from_user.username,
        photo=await get_profile_photo(message.chat.id),
        is_staff=True,
        is_superuser=True

    )
    await bot.send_message(
        message.from_user.id,
        'Користувач успішно створений\n'
        'Данні для входу: \n'
        'Логін' + f'-  {message.from_user.username}\n'
        'Пароль' + f'-  {data["password"]}\n'
        'Ви можете увійти за цим посиланням'
    )
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
