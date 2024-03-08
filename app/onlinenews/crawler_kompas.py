import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
from decouple import config
from ..logging import logger
# scrape url 
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
                    title_elem = soup.find('h1', {"class": "read__title"})
                    if title_elem:
                        title_text = title_elem.text.strip()
                    else:
                        title_text = "Title not found"  
                        
                    #     # Content Berita
                    body_elem = soup.find('div', {"class": "read__content"})
                        
                    if body_elem:
                        content_elem = body_elem.find_all('p')
                        content_text = ""
                        for p in content_elem:
                                content_text += p.text.strip() + "\n"
                            
                        if content_text.strip():
                            content_text=content_text
                            content_text = content_text.replace('\n', '').replace('\r', '').replace('\t', '')
                            content_text = ' '.join(content_text.split())
                        else:
                            content_text="Content not found"
                    else:
                            content_text="Content not found"

                    return{
                        'title': title_text,
                        'content':content_text,
                        'link' : url}
                elif response.status_code == 429:
                    logger.info({
                        "message": f"Received a 429 error for {url}. Retrying in 5 seconds..."
                    })
                    time.sleep(5)
                elif response.status_code == 403:
                    logger.info({
                        "message": f"Received a 403 error for {url}. Retrying in 90 seconds..."
                    })
                    time.sleep(90)
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
                time.sleep(5)  # You can adjust the delay as needed
    return None         

def scrape_links(date,page_number,max_retries=int(config('MAX_RETRIES'))):
    retries = 0
    while retries < max_retries:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
            }
            url = f"https://indeks.kompas.com/?site=nasional&date={date}&page={page_number}"
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                articles = soup.find_all('h3', {"class": "article__title article__title--medium"})
                links = []
                for article in articles:
                    link = article.find('a')['href']
                    links.append(link)
                logger.success({
                    "message": f"Scraped {len(links)} links from page {page_number} when {date}"
                    })
                return links
            elif response.status_code==403:
                logger.info({
                    "message":f"Received a 403 error for {url}. Retrying in 90 seconds..."
                })
                time.sleep(90)
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
                time.sleep(5)  # You can adjust the delay as needed
    return None 

def scrape_link_per_day(date, max_threads=int(config('MAX_THREAD_POOL'))):
    page_number = 1
    page_links = []

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = []

        while True:
            future = executor.submit(scrape_links, date, page_number)
            futures.append(future)
            page_number += 1

            # Break the loop if no more articles are found
            if not future.result():
                break

        for future in concurrent.futures.as_completed(futures):
            page_links.extend(future.result())

    return page_links