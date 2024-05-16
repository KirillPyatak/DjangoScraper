from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from time import sleep
from random import randint
import re


def parse_publications(driver):
    try:
        # Ожидаем появления всех строк с информацией о публикациях
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//tr[contains(@id, 'arw')]")
            )
        )
    except:
        print("Строки с информацией о публикациях не найдены")
        return

    # Находим все элементы tr с информацией о публикациях
    publication_rows = driver.find_elements(By.XPATH, "//tr[contains(@id, 'arw')]")

    for row in publication_rows:
        try:
            # Получаем номер публикации
            publication_number_element = row.find_element(By.XPATH, ".//font/b")
            publication_number = publication_number_element.text.strip()

            # Название публикации
            title_element = row.find_element(By.XPATH, ".//span")
            title = title_element.text.strip()

            # Авторы
            authors_element = row.find_element(By.XPATH, ".//i")
            authors = authors_element.text.strip()

            # Информация о публикации
            journal_info_elements = row.find_elements(
                By.XPATH, ".//a[contains(@href, 'contents.asp')]"
            )
            journal_info_text = ""
            publication_link = ""
            year = None  # Initialize year variable
            for element in journal_info_elements:
                if element.get_attribute("href"):
                    journal_info_text += element.text.strip() + ". "
                    publication_link = element.get_attribute("href")
                else:
                    journal_info_text += element.text.strip() + " "

            # Search for the year within the entire journal info string
            year_match = re.search(r"\b\d{4}\b", journal_info_text)
            if year_match:
                year = year_match.group(0)

            # Выводим данные о публикации
            print("НОМЕР ПУБЛИКАЦИИ:", publication_number)
            print("НАЗВАНИЕ:", title)
            print("АВТОРЫ:", authors)
            print("Журнал и публикация:", journal_info_text)
            if publication_link:
                print("Ссылка на публикацию:", publication_link)
            if year:
                print("Год публикации:", year)
            print()
            with open('pubs.txt', 'a') as file:
                file.write(
                    f'"НОМЕР ПУБЛИКАЦИИ:", {publication_number}\n"НАЗВАНИЕ:", {title}\n"АВТОРЫ:", {authors}\n"Журнал и публикация:", {journal_info_text}\n"Ссылка на публикацию:", {publication_link}\n"Год публикации:", {year}\n\n')
                print('Данные записались в файл pubs.txt')
        except Exception as e:
            print("Ошибка при парсинге публикации:", e)


def scrape(url):
    # Инициализируем веб-драйвер
    driver = webdriver.Firefox()
    url_ = "https://www.elibrary.ru/"
    # Входим на сервис
    driver.get(url_)
    username = "Bladdick"
    password = "Popov2002-"
    try:
        # Ожидаем появления поля для ввода логина
        print("FOO")
        sleep(2)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "login"))
        )
    except:
        print("Поле для ввода логина не найдено")
        return

    username_field = driver.find_element(By.ID, "login")
    password_field = driver.find_element(By.ID, "password")
    username_field.send_keys(username)
    password_field.send_keys(password)

    try:
        # Ожидаем активации кнопки входа
        sleep(2)
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[@class='butred' and contains(text(), 'Вход')]")
            )
        )
    except:
        print("Кнопка входа не активирована")
        return

    login_button = driver.find_element(
        By.XPATH, "//div[@class='butred' and contains(text(), 'Вход')]"
    )
    login_button.click()

    # Дождемся входа
    sleep(2)
    WebDriverWait(driver, 20).until(EC.url_changes(url))

    # Теперь мы авторизованы, найдем ссылку на страницу со списком публикаций
    try:
        # Ожидаем появления ссылки на страницу со списком публикаций
        print("BAAAZ")
        driver.get(url)
        sleep(randint(2, 10))
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//a[contains(@href, 'author_items')]")
            )
        )
    except:
        print("Ссылка на страницу со списком публикаций не найдена")
        return

    publication_link = driver.find_element(
        By.XPATH, "//a[contains(@href, 'author_items')]"
    )
    publication_link.click()

    # Дождемся загрузки страницы со списком публикаций
    try:
        # Ожидаем появления всех строк с информацией о публикациях
        print("BIIIZ")
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//tr[contains(@id, 'arw')]")
            )
        )
    except:
        print("Строки с информацией о публикациях не найдены")
        return

    # Парсим данные со страницы
    parse_publications(driver)

    # Проверяем наличие кнопки "Следующая страница"
    next_page_button = driver.find_elements(
        By.XPATH, "//a[contains(@title, 'Следующая страница')]"
    )

    # Пока кнопка "Следующая страница" присутствует, переходим на следующую страницу и парсим данные
    while next_page_button:
        try:
            # Ожидаем активации кнопки "Следующая страница"
            sleep(randint(1,3))
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//a[contains(@title, 'Следующая страница')]")
                )
            )
        except:
            print("Кнопка 'Следующая страница' не активирована")
            break

        next_page_button[0].click()
        sleep(5)  # Добавляем задержку для загрузки страницы
        # Парсим данные со страницы
        parse_publications(driver)
        next_page_button = driver.find_elements(
            By.XPATH, "//a[contains(@title, 'Следующая страница')]"
        )

    # Закрываем веб-драйвер
    driver.quit()


if __name__ == "__main__":
    url = "https://elibrary.ru/author_profile.asp?authorid=1092485"
    scrape(url)
