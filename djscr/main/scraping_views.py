from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver

def get_source_html(driver, filename):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(driver.page_source)
    except Exception as ex:
        print(ex)

def parse_articles_table(soup):
    # Assuming each article is within a <tr> (table row) element
    article_rows = soup.select('table#your_table_id tr')  # Adjust the selector based on your HTML structure

    for row in article_rows:
        # Extracting the title of the article (adjust the selector accordingly)
        title_element = row.select_one('td.title_column')  # Adjust the selector based on your HTML structure
        if title_element:
            title = title_element.get_text(strip=True)
            print(f"Article Title: {title}")

def main():
    service = Service(executable_path='C:/Users/user/Downloads/chromedriver_win32/chromedriver.exe')
    options = Options()

    # Включаем headless-режим с использованием add_argument
    options.add_argument('--headless')

    # Используем библиотеку fake-useragent для получения случайного User-Agent
    user_agent = UserAgent().random
    options.add_argument(f"user-agent={user_agent}")

    driver = webdriver.Chrome(service=service, options=options)

    # Откройте страницу входа
    login_url = "https://www.elibrary.ru/defaultx.asp"
    driver.get(login_url)

    # Найдите элементы для ввода имени пользователя и пароля, и введите свои учетные данные
    username_field = driver.find_element(By.ID, "login")
    password_field = driver.find_element(By.ID, "password")
    username = "kirillpyatak"
    password = "Kirkir2002-"
    username_field.send_keys(username)
    password_field.send_keys(password)

    # Найдите и кликните на кнопку "Вход"
    login_button = driver.find_element(By.XPATH, "//div[@class='butred' and contains(text(), 'Вход')]")
    login_button.click()

    time.sleep(3)

    # Найти все ссылки с числами и перейти на следующую страницу
    number_links = driver.find_elements(By.XPATH, "//a[contains(@href, 'author_items.asp?orgsid=')]")
    for link in number_links:
        link.click()
        # Дождитесь загрузки новой страницы
        wait = WebDriverWait(driver, 10)
        wait.until(EC.staleness_of(link))
        # Получите содержимое новой страницы
        new_page_content = driver.page_source
        # Используйте BeautifulSoup для парсинга данных на новой странице
        soup = BeautifulSoup(new_page_content, 'html.parser')

        # Пример использования функции для парсинга таблицы со статьями
        parse_articles_table(soup)

        # Скачать страницу
        page_number = link.text
        filename = f"page_{page_number}.html"
        get_source_html(driver, filename)

    driver.quit()

if __name__ == "__main__":
    main()
