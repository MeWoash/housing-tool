import os
from dotenv import load_dotenv
from loguru import logger
from pathlib import Path

is_loaded = load_dotenv()
if not is_loaded:
    logger.warning("Environment variables not loaded. Check your .env file.")

SCRAPED_DATA_DIR = Path(os.getenv("SCRAPED_DATA_DIR", "./scraped_data"))
POOL = 1
BATCH_SIZE = 1