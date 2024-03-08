from fastapi import FastAPI
from .config import SQLite3Connection
from .logging import logger
from .job import JobScheduler
from .routes import router

import os, signal

api = FastAPI()
job_scheduler = JobScheduler()
db = SQLite3Connection()

@api.on_event("startup")
def open_pool():
    logger.info(f"Opening database connection")
    SQLite3Connection().get_connection()

@api.on_event("startup")
async def startup():
    logger.info(f"Start cronjob..")
    job_scheduler.start_job_crawler()

@api.on_event("shutdown")
def close_pool():
    logger.info(f"Close database connection")
    SQLite3Connection().close_connection()

@api.on_event("shutdown")
async def shutdown():
    logger.info(f"stop cronjob..")
    job_scheduler.shutdown_job_crawler()
    os.kill(os.getpid(), signal.SIGKILL)
    
api.include_router(router)