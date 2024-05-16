import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

def parse_articles_table(soup):
    table_rows = soup.select('table tr')
    for row in table_rows[1:]:
        article_title = row.select_one('td.select-tr-left a span').text
        year = row.select_one('td:nth-of-type(2)').text
        print('Название статьи:', article_title)
        print('Год выпуска:', year)
        print('---')

def scrape(url):
    # Сгенерируем случайный User-Agent
    user_agent = UserAgent().random
    headers = {'User-Agent': user_agent}

    # Отправим GET-запрос к странице
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Функции для извлечения данных
        def find_publication_count(soup):
            publications_element = soup.find('td', class_='midtext', string='Число публикаций в РИНЦ')
            if publications_element:
                publication_count = publications_element.find_next('a').text
                return publication_count
            else:
                return None

        def find_Hirsh(soup):
            publications_element = soup.find('td', class_='midtext', string='Индекс Хирша по всем публикациям на elibrary.ru')
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

        # Извлекаем данные со страницы
        print('ВУЗ:' + find_vuz_name(soup))
        print('Число публикаций в РИНЦ:' + find_publication_count(soup))
        print('Индекс Хирша по всем публикациям на elibrary.ru:' + find_Hirsh(soup))

        # Парсим таблицу со статьями
        parse_articles_table(soup)
    else:
        print("Ошибка при получении страницы")

if __name__ == '__main__':
    url = 'https://elibrary.ru/author_profile.asp?authorid=1092485'
    scrape(url)
