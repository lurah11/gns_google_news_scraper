from selenium.webdriver.chrome.service import Service 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pytz 
import pandas as pd

# constants 

base_url = 'https://news.google.com/'


def init_driver(): 
    options = Options()
    options.headless=True
    service = Service('./chromedriver')
    driver = webdriver.Chrome(service=service,options=options)
    return driver


def get_allowed_date(): 
    tz = pytz.timezone('UTC')
    now = datetime.now(tz=tz)
    two_days_ago = now-timedelta(days=2)
    return two_days_ago

def get_news_time(article): 
    news_time = article.select('div > time')[0]
    news_time_exact = news_time.get('datetime')[:-1]
    news_time_exact = news_time_exact + "+0000"
    time_of_news = datetime.strptime(news_time_exact,"%Y-%m-%dT%H:%M:%S%z")
    return time_of_news 

def get_title(article): 
    title = article.select('h3 > a')[0].text
    return title 

def get_link(article): 
    link_a = article.select('h3 > a')[0]
    href = link_a.get('href')[2:]
    mod_href = f"{base_url}{href}"
    return mod_href



def scrap_data(driver,query): 
    result_dict = {
        'topic':[],
        'title':[],
        'date':[],
        'link':[]
    }

    driver.get(f'{base_url}search?q={query}')
    bs = BeautifulSoup(driver.page_source, 'lxml')
    articles = bs.select('article')
    for article in articles : 
        allowed_date = get_allowed_date()
        news_time = get_news_time(article)
        if allowed_date > news_time : 
            continue 
        else : 
            title = get_title(article)
            print(title)
            if (query.lower() not in title.lower()): 
                print("lala")
                continue
            else : 
                link = get_link(article)
        
        result_dict['topic'].append(query)
        result_dict['title'].append(title)
        result_dict['link'].append(link)
        result_dict['date'].append(news_time)
    df = pd.DataFrame(result_dict)
    return df




