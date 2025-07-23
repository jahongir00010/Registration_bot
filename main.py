import asyncio
import logging
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv

from registration import router as registration_router
from token_storage import is_token_used, save_used_token

load_dotenv()

async def main():
    bot = Bot(
        token=getenv("BOT_TOKEN"),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(registration_router)

    @dp.message(CommandStart(deep_link=True))
    async def cmd_start_with_token(message: Message):
        # start tokenni ajratish (masalan, /start abc123)
        token = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else None

        if not token:
            await message.answer("❌ Token topilmadi.")
            return

        if is_token_used(token):
            await message.answer("❌ Bu QR havola allaqachon ishlatilgan.")
            return

        save_used_token(token)
        await message.answer(
            f"✅ Xush kelibsiz! Sizning tokeningiz: <code>{token}</code>\n"
            f"Ro'yxatdan o'tish  uchun 'ro'yxatdan o'tish' deb yozing."
        )

    @dp.message(CommandStart())
    async def cmd_start(message: Message):
        await message.answer(
            "Assalomu alaykum!\nRo'yxatdan o'tish uchun 'ro'yxatdan o'tish' deb yozing."
        )

    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
