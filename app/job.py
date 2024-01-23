import threading
import schedule
import asyncio
from decouple import config
from .logging import logger


TASK_CRAWLING_STOP_FLAG: threading.Event = threading.Event()
TASK_CRAWLING_CRON_THREAD: threading.Thread = None


def start_job_crawler():
    global TASK_CRAWLING_CRON_THREAD, TASK_CRAWLING_STOP_FLAG
    schedule_time=int(config('TIME_INTERVAL'))

    logger.info({
                "message":f"starting crawler.."
    })
    
    # schedule.every(schedule_time).seconds.do(lambda: asyncio.run(crawling_onlinenews_day_async()))

    def run():
        while True:
            schedule.run_pending()
            if TASK_CRAWLING_STOP_FLAG.is_set():
                if TASK_CRAWLING_STOP_FLAG.is_set():
                    break
                asyncio.sleep(1)

    TASK_CRAWLING_CRON_THREAD = threading.Thread(target=run)
    TASK_CRAWLING_CRON_THREAD.start()


def shutdown_job_crawler():
    global TASK_CRAWLING_CRON_THREAD, TASK_CRAWLING_STOP_FLAG
    
    logger.info({
                "message":f"shutdown crawler.."
    })
    
    TASK_CRAWLING_STOP_FLAG.set()
    schedule.clear()

    if TASK_CRAWLING_CRON_THREAD is not None:
        TASK_CRAWLING_CRON_THREAD.join(1)
        TASK_CRAWLING_CRON_THREAD = None 