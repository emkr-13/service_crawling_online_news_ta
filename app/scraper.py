from .onlinenews import crawler_cnn, crawler_detik, crawler_kompas
from .helper import Function_QUERY
from .logging import logger
import datetime as dt
import concurrent.futures
from decouple import config

max_thread_count = int(config('MAX_THREAD_POOL'))

NEWS_CRAWLERS = {
    'Detik News': crawler_detik,
    'CNN News': crawler_cnn,
    'Kompas News': crawler_kompas
}

# List Berita
LIST_ONLINE_NEWS = ['Detik News', 'CNN News', 'Kompas News']

# Testing Berita
# LIST_ONLINE_NEWS = ['Detik News']

def scrape_and_produce_url(url, progress_time, name_news, scraper_func):
    try:
        cek_berita = Function_QUERY.get_count_news(url)
        if cek_berita == 0:
            data = scraper_func.scrape_url(url)
            if data and data.get('content') and data.get('title'):
                Function_QUERY.add_news(data['title'], progress_time, data['content'], url, name_news)
            else:
                logger.warning({"message": f"Data content or Title not found at {url} when news date {progress_time}"})
        else:
            logger.info(f"URL already exists in the database: {url}")
    except Exception as e:
        logger.error({"message": f"An error occurred while scraping and producing URL {url}: {str(e)}"})

def crawling_online_news_day():
    try:
        tasks = Function_QUERY.get_progress_online_news()
        today = dt.date.today()

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_thread_count) as executor:
            futures = []

            for task in tasks:
                news_id = task.id
                name_news = task.name
                progress_time_str = task.progress_time
                scraper_func = NEWS_CRAWLERS.get(name_news)

                progress_time = dt.datetime.strptime(progress_time_str, "%Y-%m-%d").date()

                if progress_time <= today and name_news in LIST_ONLINE_NEWS:
                    futures.append(executor.submit(crawl_and_produce_news, scraper_func, name_news, progress_time, news_id))

            # Wait for all futures to complete
            concurrent.futures.wait(futures)

    except Exception as e:
        logger.error({"message": f"An unexpected error occurred: {str(e)}"})

def crawl_and_produce_news(scraper_func, name_news, progress_time, news_id):
    try:
        logger.success({"message": f"Start Scraping {scraper_func.__name__} when news date {progress_time}"})
        all_links = scraper_func.scrape_link_per_day(progress_time)

        logger.info({"message": f"Total Links: {len(all_links)}"})

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_thread_count) as executor:
            futures = [executor.submit(scrape_and_produce_url, url, progress_time, name_news, scraper_func) for url in all_links]

            # Wait for all futures to complete
            concurrent.futures.wait(futures)

        progress_time += dt.timedelta(days=1)
        Function_QUERY.update_time_progress_time(news_id, progress_time)

    except Exception as e:
        logger.error({"message": f"An error occurred: {str(e)}"})