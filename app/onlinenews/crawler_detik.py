import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from decouple import config
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import threading
from ..logging import logger


#script di buat get URL  
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

                    # Title Element
                    title_elem = soup.find('h1', {"class": "detail__title"})
                    title_text = title_elem.text.strip() if title_elem else "Title not found"
                    # date Element
                    # nama_bulan = {
                    #     'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
                    #     'Mei': '05', 'Jun': '06', 'Jul': '07', 'Ags': '08',
                    #     'Sep': '09', 'Okt': '10', 'Nov': '11', 'Des': '12'
                    # }
                    # date_elem = soup.find('div', {"class": "detail__date"})
                    # date_text = date_elem.text.strip() if date_elem else "Date not found"
                    
                    # # Pisahkan tanggal menjadi komponen yang sesuai
                    # parts = date_text.split()
                    # hari = parts[1]
                    # bulan = nama_bulan[parts[2]]
                    # tahun = parts[3]
                    # waktu = parts[4]

                    # tanggal_dikonversi = f"{tahun}-{bulan}-{hari}"
                    # body element 
                    body_elem = soup.find('div', {"class": "detail__body"})
                    if body_elem:
                        content_elem = body_elem.find_all('p')
                        content_text = "\n".join(p.text.strip() for p in content_elem)
                        content_text = content_text.replace('\n', '').replace('\r', '').replace('\t', '')
                        content_text = ' '.join(content_text.split())
                        content_text = content_text.replace("ADVERTISEMENT SCROLL TO CONTINUE WITH CONTENT", "")
                        content_text= content_text.replace("ADVERTISEMENTSCROLL TO CONTINUE WITH CONTENT","")
                    else:
                        content_text = "Content not found"

                    return {
                        'title': title_text,
                        'content': content_text,
                        'link': url
                    }
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
                time.sleep(10)  
    return None 