from __future__ import annotations
from loguru import logger
import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from loguru import Logger

def configure_logger(name: str, log_level: str = "INFO") -> Logger:
    """Configure a named logger (ui/api/etc.) and return the global Loguru instance."""
    log_dir = os.path.join(os.getcwd(), f"logs/{name}")
    os.makedirs(log_dir, exist_ok=True)

    log_path = os.path.join(log_dir, f"{name}_{{time:YYYY-MM-DD}}.log")

    logger.remove() #remove default handler
    logger.add( #add file handler
        log_path,
        rotation="10 MB",
        retention="7 days",
        compression="zip",
        level=log_level,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level:<8} | {message}",
        enqueue=True
    )

    logger.add( #add console handler
        lambda msg: print(msg, end=""),
        level=log_level,
        format="<green>{time:HH:mm:ss}</green> | <level>{level:<8}</level> | {message}"
    )

    return logger