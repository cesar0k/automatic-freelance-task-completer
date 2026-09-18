"""Telegram bot entrypoint (aiogram 3)."""

from __future__ import annotations

import asyncio
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from loguru import logger

from services.tg_bot.config import settings
from services.tg_bot.handlers import admin, common, dev, sales

logger.remove()
logger.add(sys.stderr, level=os.getenv("LOG_LEVEL", "INFO"))


async def amain() -> None:
    logger.info("tg_bot started (BOT_TOKEN set: {})", bool(os.getenv("BOT_TOKEN")))

    bot = Bot(
        token=settings.BOT_TOKEN.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp = Dispatcher()
    dp.include_routers(common.router, admin.router, dev.router, sales.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


def main() -> None:
    asyncio.run(amain())


if __name__ == "__main__":
    main()
