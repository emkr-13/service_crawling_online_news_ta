from . import main
from .helper import Function_QUERY
from fastapi import APIRouter
from fastapi.responses import ORJSONResponse
from .schema import ListProgressOnlineNews


router = APIRouter()

@router.get("/progress_online_news",tags=["progress_online"])
async def get_list_progress_online_news():
    success= Function_QUERY.get_progress_online_news(main.db)
    return ORJSONResponse({"code": 0, "content": success})

@router.get("/single_progress_online_news/{news_id}",tags=["progress_online"])
async def get_single_progress_online_news(news_id: str):
    success= Function_QUERY.get_single_progress_online_news(news_id,main.db)
    return ORJSONResponse({"code": 0, "content": success})