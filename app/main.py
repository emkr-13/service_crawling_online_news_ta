from fastapi import FastAPI
from .config import SQLite3Connection
from .logging import logger

api = FastAPI()
pool = SQLite3Connection()

@api.on_event("startup")
def open_pool():
    logger.info(f"Opening database connection")
    pool.get_connection()

# Rest of your FastAPI code...
@api.on_event("shutdown")
def close_pool():
    logger.info(f"Close database connection")
    pool.close_connection()