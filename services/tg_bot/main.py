"""Telegram bot entrypoint (aiogram 3)."""

from __future__ import annotations

import asyncio
import os
import sys

from loguru import logger

logger.remove()
logger.add(sys.stderr, level=os.getenv("LOG_LEVEL", "INFO"))


async def amain() -> None:
    logger.info("tg_bot started (BOT_TOKEN set: {})", bool(os.getenv("BOT_TOKEN")))
    logger.info("TODO: initialise aiogram Bot + Dispatcher here.")


def main() -> None:
    asyncio.run(amain())


if __name__ == "__main__":
    main()
