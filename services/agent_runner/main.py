"""Agent runner entrypoint."""

from __future__ import annotations

import asyncio
import os
import sys

from loguru import logger

logger.remove()
logger.add(sys.stderr, level=os.getenv("LOG_LEVEL", "INFO"))


async def amain() -> None:
    logger.info("agent_runner started.")
    logger.info("TODO: execute coding agent against storage/tasks/<order_id>.")


def main() -> None:
    asyncio.run(amain())


if __name__ == "__main__":
    main()
