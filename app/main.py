from fastapi import FastAPI
from .config import SQLite3Connection
from .logging import logger
from .funcation_query import Function_QUERY

api = FastAPI()
pool = SQLite3Connection()

@api.on_event("startup")
def open_pool():
    logger.info(f"Opening database connection")
    pool.get_connection()
    
@api.get("/progress_online_news")
async def get_progress_online_news():
    return  Function_QUERY.get_progress_online_news()

@api.on_event("shutdown")
def close_pool():
    logger.info(f"Close database connection")
    pool.close_connection()