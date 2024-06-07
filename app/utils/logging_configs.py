from loguru import logger

import os

os.makedirs("logs", exist_ok=True)

logger = logger.bind(name="app")
logger.remove()
logger.add(
    "logs/app.log",
    format="{time} {level} {message}",
    level="INFO",
    rotation="100 MB",
    retention="7 days",
    compression="zip",
)
