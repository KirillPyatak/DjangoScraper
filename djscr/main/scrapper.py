# myapp/scraper.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

def scrape(soup):
    # Здесь выполняется парсинг страницы и извлечение необходимых данных
    service = Service(
        executable_path='C:/Users/user/Downloads/chromedriver_win32/chromedriver.exe')
    options = Options()
    options.add_argument('--headless')
    user_agent = UserAgent().random
    options.add_argument(f'user-agent={user_agent}')
    driver = webdriver.Chrome(service=service, options=options)
    url = 'https://elibrary.ru/author_profile.asp?authorid=830035'
    driver.get(url)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    return {
        'vuz': find_vuz_name(soup),
        'author': find_author_name(soup),
        'publication_count': find_publication_count(soup),
        'hirsh': find_Hirsh(soup),
    }

def find_publication_count(soup):
    publications_element = soup.find('td', class_='midtext', string='Число публикаций в РИНЦ')
    if publications_element:
        publication_count = publications_element.find_next('a').text
        return publication_count
    else:
        return None

def find_Hirsh(soup):
    publications_element = soup.find('td', class_='midtext',
                                     string='Индекс Хирша по всем публикациям на elibrary.ru')
    if publications_element:
        publication_hirsh = publications_element.find_next('a').text
        return publication_hirsh
    else:
        return None

def find_vuz_name(soup):
    items = soup.find_all('div')
    div_num = 0
    for n, i in enumerate(items, start=0):
        tags = i.find_all('span', class_='aster')
        for j in tags:
            if j.text == '*':
                div_num = n
    vuz_element = items[div_num].find('a')
    if vuz_element:
        return vuz_element.text
    else:
        return None

def find_author_name(soup):
    items = soup.find_all('div')
    div_num = 0
    for n, i in enumerate(items, start=0):
        tags = i.find_all('span', class_='aster')
        for j in tags:
            if j.text == '*':
                div_num = n
    return items[div_num].find('b').text
