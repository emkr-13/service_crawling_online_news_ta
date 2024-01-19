from fastapi import FastAPI
from .config import SQLite3Connection

api = FastAPI()
pool = SQLite3Connection()

@api.on_event("startup")
def open_pool():
    print("start open pool connection..")
    pool.get_connection()

# Rest of your FastAPI code...
