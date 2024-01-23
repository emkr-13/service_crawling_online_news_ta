from .import main
from .schema import ListProgressOnlineNews
from .logging import logger

class Function_QUERY:
    # Get List Progress Online News
    @staticmethod
    def get_progress_online_news():
        try:
            QUERY = 'SELECT id,name,since_time,progress_time,until_time FROM progress_online_news'
            logger.info(f"Executing query: {QUERY}")
            data = main.pool.execute_query(QUERY)
            result = [ListProgressOnlineNews(*row) for row in data]
            logger.info(f"Retrieved data: {result}")
            return result
        except Exception as e:
            logger.error(f"Error in get_progress_online_news: {str(e)}")
            raise
        
    @staticmethod
    def get_single_progress_online_news(news_id):
        try:
            QUERY = 'SELECT id,name,since_time,progress_time,until_time FROM progress_online_news WHERE id=?'
            logger.info(f"Executing query: {QUERY}")
            data = main.pool.select_where_query(QUERY, (news_id,))
            if data:
                result = ListProgressOnlineNews(*data[0])
                logger.info(f"Retrieved data: {result}")
                return result
            else:
                logger.info(f"No data found for ID: {news_id}")
                return None
        except Exception as e:
            logger.error(f"Error in get_single_progress_online_news: {str(e)}")
            raise