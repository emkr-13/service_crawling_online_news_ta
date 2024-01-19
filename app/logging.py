from loguru import logger
from pathlib import Path
from datetime import datetime
from decouple import config
import os
import sys

log_dir = config("LOG_DIR", "logs")
Path(log_dir).mkdir(exist_ok=True)
log_format = "<level>{level: <8}</level> " "<green>{time:YYYY-MM-DD HH:mm:ss}</green> " "<level>{message}</level>"
logger.remove()
logger.add(sys.stdout, format=log_format, level="DEBUG")
logger.add(
    os.path.join(log_dir, f"{datetime.now().date()}.log"),
    rotation="1 days",
    retention="7 days",
    format=log_format,
    level="INFO",
)