import sqlite3

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
