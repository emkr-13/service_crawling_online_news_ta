from .import main
from .schema import ListOnlineNews, OnlineNews
from .logging import logger

class Function_QUERY:
    # Get List Progress Online News
    @staticmethod
    def get_progress_online_news():
        QUERY = 'SELECT * FROM progress_online_news'
        logger.info(f"Executing query: {QUERY}")
        data = main.pool.execute_query(QUERY)
        logger.info(f"Retrieved data: {data}")
        
        return data
    # Get List Online News
    @staticmethod
    def get_list_online_news():
        QUERY = (
            'SELECT * FROM online_news'
        )
        data=main.pool.execute_query(QUERY)
        return [OnlineNews(*x) for x in data]