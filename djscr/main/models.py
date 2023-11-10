# models.py
from django.db import models

class ScrapedData(models.Model):
    vuz = models.CharField(max_length=255, blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    publication_count = models.CharField(max_length=255, blank=True, null=True)
    hirsh = models.CharField(max_length=255, blank=True, null=True)
    vac = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.vuz
