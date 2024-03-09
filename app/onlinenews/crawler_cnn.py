import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from decouple import config
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import threading
from ..logging import logger


def scrape_url(url,max_retries=int(config('MAX_RETRIES'))):
    retries = 0
    while retries < max_retries:
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
                }
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')   
                    # Judul Berita
                    title_elem = soup.find('h1', {"class": "mb-2 text-[28px] leading-9 text-cnn_black"})
                    if title_elem:
                        title_text = title_elem.text.strip()
                    else:
                        title_text = "Title not found"     
                    #     # Content Berita
                    body_elem = soup.find('div', {"class": "detail-text text-cnn_black text-sm grow min-w-0"})
                    
                    if body_elem:
                        content_elem = body_elem.find_all('p')
                        content_text = ""
                        for p in content_elem:
                            content_text += p.text.strip() + "\n"
                        
                        if content_text.strip():
                            content_text=content_text
                            content_text = content_text.replace('\n', '').replace('\r', '').replace('\t', '')
                            content_text = ' '.join(content_text.split())
                            content_text = content_text.replace("ADVERTISEMENT SCROLL TO CONTINUE WITH CONTENT", "")
                            content_text = content_text.replace("ADVERTISEMENTSCROLL TO CONTINUE WITH CONTENT","")
                        else:
                            content_text ="Content not found"
                    else:
                        content_text ="Content not found"
                    return {
                        'title': title_text,
                        'content': content_text,
                        'link': url
                    }
                elif response.status_code == 429:
                    logger.info({
                        "message": f"Received a 429 error for {url}. Retrying in 5 seconds..."
                    })
                    time.sleep(5)
                else:
                    logger.error(
                        {"message": f"Failed to retrieve data from {url}: Status Code {response.status_code}"}
                        )
            except requests.exceptions.RequestException as e:
                logger.error({
                    "message":f"Error fetching URL '{url}': {e}"
                })
            except Exception as e:
                logger.error({
                    "message":f"Error processing URL '{url}': {e}"
                })
            retries += 1
            if retries < max_retries:
                logger.info({
                    "message":f"Retrying {url} (Attempt {retries}/{max_retries})"
                })
                time.sleep(5)  
    return None 

# scrap url per day 
def scrape_links_news(date,page_number):
    formatted_date = date.strftime("%Y/%m/%d")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    }
    url = f"https://www.cnnindonesia.com/nasional/indeks/3/{page_number}?date={formatted_date}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    div_badan = soup.find('div', {"class": "flex flex-col gap-5"})
    if div_badan:
        articles = div_badan.findAll('article', {"class": "flex-grow"})
        links = []
        for article in articles:
            link = article.find('a')['href']
            links.append(link)
    else:
        logger.error(f"Div 'flex flex-col gap-5' not found on page {page_number}")

    logger.success({
        "message": f"Scraped {len(links)} links from page {page_number} when {date} from www.cnnindonesia.com"
        })
    
    return links

# multi threead
def scrape_link_per_day(date,max_threads=int(config('MAX_THREAD_POOL'))):
    page_number = 0
    page_links = []

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = []

        while True:
            future = executor.submit(scrape_links_news, date,page_number)
            futures.append(future)
            page_number += 1

            # Break the loop if no more articles are found
            if not future.result():
                break

        for future in concurrent.futures.as_completed(futures):
            page_links.extend(future.result())

    return page_links