import sqlite3
from .logging import logger

class SQLite3Connection:
    __db__: str
    con: sqlite3.Connection

    def __init__(self):
        self.__db__ = "onlinenews.db"
        assert self.database_exists(), f"The database '{self.__db__}' does not exist."

    def database_exists(self):
        try:
            # Attempt to connect to the database
            with sqlite3.connect(self.__db__):
                pass
            return True
        except sqlite3.OperationalError:
            return False

    def get_connection(self):
        self.con = sqlite3.connect(self.__db__)
        return self.con

    def close_connection(self):
        self.con.close()

    def execute_query(self, query):
        try:
            cursor = self.con.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except sqlite3.Error as e:
            logger.error(
            {"message": f"Error executing query: {e}"}
            )
            return None

    def insert_query(self, query, data):
        try:
            cursor = self.con.cursor()
            cursor.execute(query, data)
            self.con.commit()
            cursor.close()
            return True
        except sqlite3.Error as e:
            logger.error(
            {"message": f"Error inserting data: {e}"}
            )
            return False

    def update_query(self, query, data):
        try:
            cursor = self.con.cursor()
            cursor.execute(query, data)
            self.con.commit()
            cursor.close()
            return True
        except sqlite3.Error as e:
            logger.error(
            {"message": f"Error updating data: {e}"}
            )
            return False

    def select_where_query(self, query, data):
        try:
            cursor = self.con.cursor()
            cursor.execute(query, data)
            result = cursor.fetchall()
            cursor.close()
            return result
        except sqlite3.Error as e:
            logger.error(
            {"message": f"Error executing select query with WHERE clause: {e}"}
            )
            return None