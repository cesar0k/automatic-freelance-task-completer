"""Scraper entrypoint."""

from __future__ import annotations

import asyncio
import os
import sys

from loguru import logger

logger.remove()
logger.add(sys.stderr, level=os.getenv("LOG_LEVEL", "INFO"))


async def amain() -> None:
    logger.info("scraper started.")
    logger.info("TODO: poll freelance feeds and push orders to Postgres.")


def main() -> None:
    asyncio.run(amain())


if __name__ == "__main__":
    main()
