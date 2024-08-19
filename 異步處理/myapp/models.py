'''

# myapp/models.py
from django.db import models

class ScrapingResult(models.Model):
    query = models.CharField(max_length=255)
    result = models.TextField()


'''