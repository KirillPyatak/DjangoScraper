# myproject/urls.py
from django.contrib import admin
from django.urls import path, include
from main.views import index, ScrapeView, ScrapedDataAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('scrape/', ScrapeView.as_view(), name='scrape'),  # Используйте ScrapeView.as_view() для класса представления
    path('api/data/', ScrapedDataAPIView.as_view(), name='api_data'),
]
