from fastapi import FastAPI
from .config import SQLite3Connection
from .logging import logger
from .helper import Function_QUERY

api = FastAPI()
pool = SQLite3Connection()

@api.on_event("startup")
def open_pool():
    logger.info(f"Opening database connection")
    pool.get_connection()
    
@api.get("/progress_online_news")
async def get_progress_online_news():
    return  Function_QUERY.get_progress_online_news()

@api.get("/progress_online_news/{news_id}")
async def get_single_progress_online_news(news_id: int):
    news_entry = Function_QUERY.get_single_progress_online_news(news_id)
    if news_entry:
        return news_entry
    else:
        raise HTTPException(status_code=404, detail="News entry not found")

@api.on_event("shutdown")
def close_pool():
    logger.info(f"Close database connection")
    pool.close_connection()