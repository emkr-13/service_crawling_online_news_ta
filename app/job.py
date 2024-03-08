import threading
import schedule
import time
from decouple import config
from .logging import logger
from .scraper import crawling_onlinenews_day

class JobScheduler:
    TASK_CRAWLING_STOP_FLAG: threading.Event = threading.Event()
    TASK_CRAWLING_CRON_THREAD: threading.Thread = None

    @staticmethod
    def start_job_crawler():
        schedule_time = int(config('TIME_INTERVAL'))

        logger.info({
            "message": "Starting crawler.."
        })

        schedule.every(schedule_time).seconds.do(lambda: JobScheduler.run_crawling())

        def run():
            while True:
                schedule.run_pending()
                if JobScheduler.TASK_CRAWLING_STOP_FLAG.is_set():
                    if JobScheduler.TASK_CRAWLING_STOP_FLAG.is_set():
                        break
                    time.sleep(1)

        JobScheduler.TASK_CRAWLING_CRON_THREAD = threading.Thread(target=run)
        JobScheduler.TASK_CRAWLING_CRON_THREAD.start()

    @staticmethod
    def run_crawling():
        crawling_onlinenews_day()

    @staticmethod
    def shutdown_job_crawler():
        logger.info({
            "message": "Shutdown crawler.."
        })

        JobScheduler.TASK_CRAWLING_STOP_FLAG.set()
        schedule.clear()

        if JobScheduler.TASK_CRAWLING_CRON_THREAD is not None:
            JobScheduler.TASK_CRAWLING_CRON_THREAD.join(1)
            JobScheduler.TASK_CRAWLING_CRON_THREAD = None