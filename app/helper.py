from .schema import ListProgressOnlineNews
from .logging import logger
from .config import SQLite3Connection

class Function_QUERY:
    # Tabel Progress Online News        
    @staticmethod
    def get_progress_online_news(db_connection=None):
        try:
                QUERY = "SELECT id,name,since_time,progress_time,until_time FROM progress_online_news WHERE progress_time <= until_time"
                logger.info(f"Executing query: {QUERY}")

                # If db_connection is not provided, create a new SQLite connection
                if db_connection is None:
                    with SQLite3Connection() as db_connection:
                        data = db_connection.execute_query(QUERY)
                else:
                    data = db_connection.execute_query(QUERY)

                result = [ListProgressOnlineNews(*row) for row in data]
                logger.info(f"Retrieved data: {result}")
                return result
        except Exception as e:
                logger.error(f"Error in get_progress_online_news: {str(e)}")
                raise
            
    # Create Progress Online News
    @staticmethod
    def create_progress_online_news(name, since_time ,progress_time,until_time, db_connection=None):
        try:
            QUERY = 'INSERT INTO progress_online_news (name,since_time,progress_time,until_time) VALUES (?, ?,?,?)'
            data = (name, since_time,progress_time,until_time)

            # If db_connection is not provided, create a new SQLite connection
            if db_connection is None:
                with SQLite3Connection() as db_connection:
                    result = db_connection.insert_query(QUERY, data)
            else:
                result = db_connection.insert_query(QUERY, data)

            logger.info(f"Created progress_online_news entry with ID: {result}")
            return result
        except Exception as e:
            logger.error(f"Error in create_progress_online_news: {str(e)}")
            raise
    
    # Update Time Progress Time
    @staticmethod
    def update_time_progress_time(id, progress_time,db_connection=None):
        try:
            QUERY = 'UPDATE progress_online_news SET progress_time=? WHERE id=?'
            data = (progress_time, id)
            if db_connection is None:
                with SQLite3Connection() as db_connection:
                    result = db_connection.update_query(QUERY, data)
            else:
                result = db_connection.update_query(QUERY, data)
            logger.info(f"Updated progress_time for progress_online_news entry with ID: {id}")
            return result
        except Exception as e:
            logger.error(f"Error in update_time_progress_time: {str(e)}")
            raise
    ### get single progress_online_news    
    @staticmethod
    def get_single_progress_online_news(news_id,db_connection=None):
        try:
            QUERY = 'SELECT id,name,since_time,progress_time,until_time FROM progress_online_news WHERE id=?'
            data = (news_id)
            logger.info(f"Executing query: {QUERY}")
            if db_connection is None:
                with SQLite3Connection() as db_connection:
                    data = db_connection.select_where_query(QUERY,data)
            else:
                data = db_connection.select_where_query(QUERY,data)
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
    ## Get 
    @staticmethod
    def get_count_news(url, db_connection=None):
        try:
            QUERY = "SELECT COUNT(*) FROM online_news WHERE url=?"
            data = url,
            logger.info(f"Executing query: {QUERY}")
            
            # Check if db_connection is None before using it as a context manager
            if db_connection is None:
                # Create a new connection or handle the case when db_connection is None
                with SQLite3Connection() as db_connection:
                    data = db_connection.select_where_query(QUERY, data)
            else:
                # Use the existing connection
                data = db_connection.select_where_query(QUERY, data)
                
            if data:
                result = data[0][0]
                logger.info(f"Retrieved data: {result}")
                return result
            else:
                logger.info(f"No data found for ID: {url}")
                return None
        except Exception as e:
            logger.error(f"Error in get_count_online_news: {str(e)}")
            raise
    
    ## Tabel Online News 
    # Fungsi add in data news 
    @staticmethod
    def add_news(title,news_published_at,content,url,asal_berita,db_connection=None):
        try:
            QUERY = 'INSERT INTO online_news (title,news_published_at,content,url,asal_berita) VALUES (?,?,?,?,?)'
            data = (title,news_published_at,content,url,asal_berita)

            # If db_connection is not provided, create a new SQLite connection
            if db_connection is None:
                with SQLite3Connection() as db_connection:
                    result = db_connection.insert_query(QUERY, data)
            else:
                result = db_connection.insert_query(QUERY, data)

            logger.success(f"add news with ID: {result} and with {url}")
            return result
        except Exception as e:
            logger.error(f"Error add news: {str(e)}")
            raise