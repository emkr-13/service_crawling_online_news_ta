import sqlite3
import os
from .logging import logger

class SQLite3Connection:
    __db__: str
    con: sqlite3.Connection

    def __init__(self):
        self.__db__ = "onlinenews.db"
        self.con = None
        assert self.database_exists(), f"The database '{self.__db__}' does not exist."

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.con:
            self.close_connection()

    def database_exists(self):
        try:
            with sqlite3.connect(self.__db__):
                pass
            return True
        except sqlite3.OperationalError:
            return False

    def get_connection(self):
        try:
            if self.con is None or not self.con.__enter__().__exit__:
                self.con = sqlite3.connect(self.__db__)
        except AttributeError:
            # Handle AttributeError by reopening connection
            self.con = sqlite3.connect(self.__db__)
        return self.con

    def close_connection(self):
        if self.con:
            self.con.close()

    def execute_query(self, query):
        try:
            cursor = self.get_connection().cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except sqlite3.Error as e:
            logger.error({"message": f"Error executing query: {e}"})
            return None

    def insert_query(self, query, data):
        try:
            cursor = self.get_connection().cursor()
            cursor.execute(query, data)
            self.con.commit()
            cursor.close()
            return True
        except sqlite3.Error as e:
            logger.error({"message": f"Error inserting data: {e}"})
            return False

    def update_query(self, query, data):
        try:
            cursor = self.get_connection().cursor()
            cursor.execute(query, data)
            self.con.commit()
            cursor.close()
            return True
        except sqlite3.Error as e:
            logger.error({"message": f"Error updating data: {e}"})
            return False

    def select_where_query(self, query, data):
        try:
            cursor = self.get_connection().cursor()
            cursor.execute(query, data)
            result = cursor.fetchall()
            cursor.close()
            return result
        except sqlite3.Error as e:
            logger.error({"message": f"Error executing select query with WHERE clause: {e}"})
            return None
        
    def delete_query(self, query, data):
        try:
            cursor = self.get_connection().cursor()
            cursor.execute(query, data)
            self.con.commit()
            cursor.close()
            return True
        except sqlite3.Error as e:
            logger.error({"message": f"Error deleting data: {e}"})
            return False