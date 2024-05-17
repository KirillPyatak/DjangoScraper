from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from random import randint
import re

def parse_internal_publication(driver, publication_link, output_file):
    try:
        sleep(randint(2, 6))
        driver.get(publication_link)
        sleep(randint(2, 6))
        annotation_element = driver.find_element(By.XPATH, "//div[@id='abstract1']")
        annotation = annotation_element.text.strip()


        # Находим элемент, содержащий информацию о вхождении в РИНЦ
        rinc_element = driver.find_element(By.XPATH, "//td[contains(text(), 'Входит в РИНЦ:')]")

        # Находим дочерний элемент, содержащий статус вхождения в РИНЦ
        rinc_status_element = rinc_element.find_element(By.TAG_NAME, 'font')

        # Получаем текст статуса вхождения в РИНЦ
        rinc_status = rinc_status_element.text.strip()

        print("Статус вхождения в РИНЦ:", rinc_status)
        print("Шаг: Парсинг внутренней публикации")
        print("Аннотация:", annotation)
        print("Вхождение в РИНЦ:", rinc_status)
        print()

        # Записываем всю информацию в файл
        with open(output_file, "a", encoding="utf-8") as file:
            file.write(f"Статус вхождения в РИНЦ: {rinc_status}\n")
            file.write(f"Аннотация: {annotation}\n")
            file.write("\n")

        # Возвращаемся к списку публикаций
        driver.back()

    except Exception as e:
        print("Ошибка при парсинге внутренней публикации:", e)

def parse_publication(driver, row, output_file):
    try:
        publication_data = {}

        publication_number_element = row.find_element(By.XPATH, ".//font/b")
        publication_data['Номер публикации'] = publication_number_element.text.strip()

        title_element = row.find_element(By.XPATH, ".//span")
        publication_data['Название'] = title_element.text.strip()

        authors_element = row.find_element(By.XPATH, ".//i")
        publication_data['Авторы'] = authors_element.text.strip()

        publication_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, ".//td[@align='left']//span[contains(@style, 'overflow-wrap: break-word;')]/a"))
        )
        publication_data['Ссылка на публикацию'] = publication_link.get_attribute("href")

        journal_info_elements = row.find_elements(By.XPATH, ".//a[contains(@href, 'contents.asp')]")
        journal_info_text = ""
        for element in journal_info_elements:
            journal_info_text += element.text.strip() + ". "

        year_match = re.search(r"\b\d{4}\b", journal_info_text)
        if year_match:
            publication_data['Год публикации'] = year_match.group(0)

        publication_data['Журнал и публикация'] = journal_info_text.strip()

        print("Шаг: Парсинг публикации")
        print(publication_data)
        print()

        if publication_data['Ссылка на публикацию']:
            sleep(randint(2, 6))
            parse_internal_publication(driver, publication_data['Ссылка на публикацию'], output_file)

        # Записываем информацию о публикации в файл
        with open(output_file, "a", encoding="utf-8") as file:
            file.write(f"Номер публикации: {publication_data['Номер публикации']}\n")
            file.write(f"Название: {publication_data['Название']}\n")
            file.write(f"Авторы: {publication_data['Авторы']}\n")
            file.write(f"Ссылка на публикацию: {publication_data['Ссылка на публикацию']}\n")
            file.write(f"Год публикации: {publication_data.get('Год публикации', 'N/A')}\n")
            file.write(f"Журнал и публикация: {publication_data['Журнал и публикация']}\n")
            file.write("\n")

    except Exception as e:
        print("Ошибка при парсинге публикации:", e)

def scrape_with_proxy(url, proxy_ip, proxy_port, proxy_username, proxy_password, output_file):
    proxy = f"https://{proxy_username}:{proxy_password}@{proxy_ip}:{proxy_port}"

    firefox_options = webdriver.FirefoxOptions()
    firefox_options.add_argument('--proxy-server=%s' % proxy)

    driver = webdriver.Firefox(options=firefox_options)

    print("Процесс начинается...")
    try:
        print("Шаг: Вход на сайт")
        url_ = 'https://elibrary.ru/'
        driver.get(url_)
        sleep(randint(2, 6))
        username = "Dmitry1237"
        password = "t78D32A99"

        username_field = driver.find_element(By.ID, "login")
        password_field = driver.find_element(By.ID, "password")
        username_field.send_keys(username)
        password_field.send_keys(password)

        login_button = driver.find_element(By.XPATH, "//div[@class='butred' and contains(text(), 'Вход')]")
        login_button.click()

        sleep(randint(2, 6))
        WebDriverWait(driver, 20).until(EC.url_changes(url_))

        print("Шаг: Переход на страницу публикаций")
        driver.get(url)
        sleep(randint(2, 6))
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'author_items')]")))

        publication_link = driver.find_element(By.XPATH, "//a[contains(@href, 'author_items')]")
        publication_link.click()

        print("Шаг: Парсинг публикаций")
        while True:
            try:
                sleep(randint(2, 6))
                WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//tr[contains(@id, 'arw')]")))
                publication_rows = driver.find_elements(By.XPATH, "//tr[contains(@id, 'arw')]")
                for row in publication_rows:
                    parse_publication(driver, row, output_file)

                next_page_button = driver.find_elements(By.XPATH, "//a[contains(@title, 'Следующая страница')]")
                if not next_page_button:
                    break

                print("Шаг: Переход на следующую страницу")
                sleep(randint(2, 6))
                next_page_button[0].click()

            except Exception as e:
                print("Ошибка при парсинге страницы:", e)
                break

    except Exception as e:
        print("Ошибка:", e)

    finally:
        driver.quit()
        print("Процесс завершен.")

if __name__ == "__main__":
    url = "https://elibrary.ru/author_profile.asp?authorid=1092485"
    proxy_ip = "80.243.134.213"
    proxy_port = "8000"
    proxy_username = "nLhxvD"
    proxy_password = "rEmasV"
    output_file = "publication_info.txt"
    scrape_with_proxy(url, proxy_ip, proxy_port, proxy_username, proxy_password, output_file)
