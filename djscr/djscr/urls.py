# myproject/urls.py
from django.contrib import admin
from django.urls import path, include
from main.views import index, scrape_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('scrape/', scrape_view, name='scrape_view'),
]
