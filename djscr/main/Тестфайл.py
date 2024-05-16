from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import time


def get_publication_links(driver):
    try:
        # Ожидаем появления всех строк с информацией о публикациях
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//tr[contains(@id, 'arw')]")))
    except:
        print("Строки с информацией о публикациях не найдены")
        return []

    # Находим все элементы tr с информацией о публикациях
    publication_rows = driver.find_elements(By.XPATH, "//tr[contains(@id, 'arw')]")
    publication_links = []

    for row in publication_rows:
        try:
            # Получаем ссылку на публикацию
            publication_link_element = row.find_element(By.XPATH, ".//a[contains(@href, '/item.asp?id=')]")
            publication_link = publication_link_element.get_attribute('href')
            publication_links.append(publication_link)
        except Exception as e:
            print("Ошибка при получении ссылки на публикацию:", e)

    return publication_links


def parse_publication(driver, publication_url):
    try:
        # Переходим на страницу публикации
        driver.get(publication_url)

        # Ждем загрузки страницы публикации
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@id='abstract1']")))

        # Получаем данные о публикации
        annotation = None
        try:
            # Пытаемся найти аннотацию по тексту "АННОТАЦИЯ:" и получить следующий элемент
            annotation_element = driver.find_element(By.XPATH, "//font[contains(text(), 'АННОТАЦИЯ:')]/following::div[1]")
            annotation = annotation_element.text.strip()
        except NoSuchElementException:
            # Если не удалось найти аннотацию по этому методу, попробуем другой способ
            try:
                # Пытаемся найти аннотацию по тексту "АННОТАЦИЯ:" и получить родительский элемент, затем следующий элемент
                annotation_element = driver.find_element(By.XPATH, "//font[contains(text(), 'АННОТАЦИЯ:')]/ancestor::table/following-sibling::div[1]")
                annotation = annotation_element.text.strip()
            except NoSuchElementException:
                # Если и это не удалось, выводим сообщение об ошибке
                print("Аннотация не найдена")

        # Получаем информацию о вхождении публикации в РИНЦ
        rinс_entry = None
        try:
            # Пытаемся найти информацию о вхождении в РИНЦ по тексту "Входит в РИНЦ:"
            rinc_element = driver.find_element(By.XPATH, "//td[contains(text(), 'Входит в РИНЦ:')]/font")
            rinс_entry = rinc_element.text.strip().lower()  # Приводим текст к нижнему регистру
        except NoSuchElementException:
            # Если не удалось найти информацию, выводим сообщение
            print("Информация о вхождении в РИНЦ не найдена")

        # Выводим информацию о публикации
        print("Парсинг информации о публикации:", publication_url)
        print("АННОТАЦИЯ:")
        print(annotation)
        print("Входит в РИНЦ:", rinс_entry if rinс_entry else "Информация отсутствует")
        print()
    except Exception as e:
        print("Ошибка при парсинге публикации:", e)



def scrape(url):
    # Инициализируем веб-драйвер
    driver = webdriver.Firefox()

    # Входим на сервис
    driver.get(url)
    username = "kirillpyatak"
    password = "Kirkir2002-"
    try:
        # Ожидаем появления поля для ввода логина
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "login")))
    except:
        print("Поле для ввода логина не найдено")
        return

    username_field = driver.find_element(By.ID, "login")
    password_field = driver.find_element(By.ID, "password")
    username_field.send_keys(username)
    password_field.send_keys(password)

    try:
        # Ожидаем активации кнопки входа
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='butred' and contains(text(), 'Вход')]")))
    except:
        print("Кнопка входа не активирована")
        return

    login_button = driver.find_element(By.XPATH, "//div[@class='butred' and contains(text(), 'Вход')]")
    login_button.click()

    # Дождемся входа
    WebDriverWait(driver, 20).until(EC.url_changes(url))

    # Теперь мы авторизованы, найдем ссылку на страницу со списком публикаций
    try:
        # Ожидаем появления ссылки на страницу со списком публикаций
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'author_items')]")))
    except:
        print("Ссылка на страницу со списком публикаций не найдена")
        return

    publication_link = driver.find_element(By.XPATH, "//a[contains(@href, 'author_items')]")
    publication_link.click()

    # Дождемся загрузки страницы со списком публикаций
    try:
        # Ожидаем появления всех строк с информацией о публикациях
        WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//tr[contains(@id, 'arw')]")))
    except:
        print("Строки с информацией о публикациях не найдены")
        return

    # Получаем ссылки на публикации
    publication_links = get_publication_links(driver)

    # Переходим по каждой ссылке на публикацию и парсим данные
    for link in publication_links:
        parse_publication(driver, link)

    # Закрываем веб-драйвер
    driver.quit()


if __name__ == '__main__':
    url = 'https://elibrary.ru/author_profile.asp?authorid=1092485'
    scrape(url)
