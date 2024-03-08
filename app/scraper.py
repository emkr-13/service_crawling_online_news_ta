from .onlinenews import crawler_cnn,crawler_detik,crawler_kompas
from .helper import Function_QUERY
from .logging import logger
import datetime as dt
import concurrent.futures
from decouple import config

max_thread_count = int(config('MAX_THREAD_POOL'))

NEWS_CRAWLERS = {
    'Detik News':crawler_detik,
    'CNN News':crawler_cnn,
    'Kompas News':crawler_kompas
}

LIST_ONLINE_NEWS = ['Detik News','CNN News','Kompas News']

def scrape_and_producer_url(url, progress_time,name_news, scraper_func):
    try:
        cek_berita=Function_QUERY.get_count_news(url)
        if cek_berita == 0:
            data = scraper_func.scrape_url(url)
            if data is None:
                logger.debug({"message": f"Data cannot be scraped from the URL: {url}"})
            else:
                if data['content'] == 'Content not found' or  data['title'] == 'Content not found':
                    logger.warning({"message": f"Data content or Title not found, {url} when news date {progress_time}"})
                else:
                    
                    Function_QUERY.add_news(url)
     
            logger.info(f"URl already exists, {url} in database")
    except Exception as e:
        logger.error({"message": f"An error occurred while scraping and producing URL {url}: {str(e)}"})

def crawling_onlinenews_day():
    try:
        task = Function_QUERY.get_progress_online_news()
        today = dt.date.today()

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_thread_count) as executor:
            futures = []

            for i in range(len(task)):
                news_id = task[i].id
                name_news = task[i].name
                since_time=task[i].since_time
                progrees_time_str = task[i].progress_time
                until_time=task[i].until_time
                scraper_func = NEWS_CRAWLERS.get(name_news)

                progrees_time = dt.datetime.strptime(progrees_time_str, "%Y-%m-%d").date()

                if progrees_time <= today and name_news in LIST_ONLINE_NEWS:
                    futures.append(executor.submit(crawl_and_produce_news, scraper_func, name_news,progrees_time, news_id,since_time,until_time))

            # Wait for all futures to complete
            concurrent.futures.wait(futures)

    except Exception as e:
        logger.error({"message": f"An unexpected error occurred: {str(e)}"})
        
        

def crawl_and_produce_news(scraper_func, name_news, progrees_time, news_id, since_time,until_time):
    try:
        start_link = dt.datetime.now()
        logger.success({"message": f"Start Scraping {scraper_func.__name__} when news date {progrees_time}"})
        
        all_link=scraper_func.scrape_link_per_day(progrees_time)
            
        end_link = dt.datetime.now()
        time_link = end_link - start_link

        logger.info({"message": f"Total Link: {len(all_link)} with time use {time_link}"})

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_thread_count) as executor:
            start = dt.datetime.now()
            futures = [executor.submit(scrape_and_producer_url, url, progrees_time, name_news, scraper_func) for url in all_link]

            # Wait for all futures to complete
            concurrent.futures.wait(futures)

            end = dt.datetime.now()
            time_taken = end - start
            logger.success({"message": f"Time for crawling {time_taken} for total links {len(all_link)} in news {scraper_func.__name__} when date {progrees_time}"})

        progrees_time += dt.timedelta(days=1)
        Function_QUERY.update_time_progress_time(news_id, progrees_time)

    except Exception as e:
        logger.error({"message": f"An error occurred: {str(e)}"})