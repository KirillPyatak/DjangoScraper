# views.py
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from selenium.webdriver.common.by import By

from .models import ScrapedData
from .serializers import ScrapedDataSerializer
from bs4 import BeautifulSoup
from rest_framework import status
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from fake_useragent import UserAgent

class ScrapedDataAPIView(APIView):
    def get(self, request):
        scraped_data = ScrapedData.objects.all()
        serializer = ScrapedDataSerializer(scraped_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

def index(request):
    return render(request, 'index.html')

class ScrapeView(APIView):
    def get(self, request):
        if request.method == 'GET':
            url = request.GET.get('url')

            try:
                # Функция для скрейпинга страницы
                def scrape(url):
                    service = Service(
                        executable_path='C:/Users/user/Downloads/chromedriver_win32/chromedriver.exe')
                    options = Options()

                    #Включаем headless-режим с использованием add_argument
                    options.add_argument('--headless')

                    # Используем библиотеку fake-useragent для получения случайного User-Agent
                    user_agent = UserAgent().random
                    options.add_argument(f"user-agent={user_agent}")

                    driver = webdriver.Chrome(service=service, options=options)

                    # Откройте страницу входа
                    login_url = "https://www.elibrary.ru/defaultx.asp"
                    driver.get(login_url)

                    # Найдите элементы для ввода имени пользователя и пароля, и введите свои учетные данные
                    username_field = driver.find_element(By.ID, "login")  # Идентификатор элемента "login"
                    password_field = driver.find_element(By.ID, "password")  # Идентификатор элемента "password"
                    username = "kirillpyatak"
                    password = "Kirkir2002-"
                    username_field.send_keys(username)
                    password_field.send_keys(password)

                    # Найдите и кликните на кнопку "Вход"
                    login_button = driver.find_element(By.XPATH, "//div[@class='butred' and contains(text(), 'Вход')]")
                    login_button.click()

                    # Теперь вы авторизованы, и вы можете получить доступ к странице, которую вы хотите получить
                    driver.get(url)
                    time.sleep(3)

                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    driver.quit()
                    return soup

                # Функции для поиска данных на странице
                def find_publication_count(soup):
                    publications_element = soup.find('td', class_='midtext', string='Число публикаций в РИНЦ')
                    if publications_element:
                        publication_count = publications_element.find_next('a').text
                        return publication_count
                    else:
                        return None

                def find_Hirsh(soup):
                    # Найдем все элементы <td> с классом "midtext"
                    td_elements = soup.find_all('td', class_='midtext')
                    for td_element in td_elements:
                        # Проверяем, содержит ли текущий <td> текст "Индекс Хирша по публикациям в РИНЦ"
                        if "Индекс Хирша по публикациям в РИНЦ" in td_element.text:
                            # Если текст найден, ищем следующий элемент <td>
                            next_td_element = td_element.find_next('td', class_='midtext')
                            # Проверяем, есть ли такой следующий элемент
                            if next_td_element:
                                # Извлекаем текст из следующего элемента <td>
                                hirsh_text = next_td_element.text.strip()
                                return hirsh_text

                    # Если ничего не найдено, возвращаем None
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

                def find_VAC(soup):
                    vac_element = soup.find('td', class_='midtext',
                                            string='Число статей в российских журналах из перечня ВАК')
                    if vac_element:
                        a_element = vac_element.find_next('a')
                        if a_element:
                            publication_vac = a_element.text
                            return publication_vac
                    return None

                # Выполнить скрейпинг и поиск данных
                soup = scrape(url)
                data = {
                    'vuz': find_vuz_name(soup),
                    'author': find_author_name(soup),
                    'publication_count': find_publication_count(soup),
                    'hirsh': find_Hirsh(soup),
                    'vac': find_VAC(soup),
                }

                # Создание и сохранение объекта ScrapedData с использованием сериализатора
                serializer = ScrapedDataSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(data, status=status.HTTP_201_CREATED)
                else:
                    return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
