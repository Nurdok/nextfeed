from django.db import models

# Create your models here.

class Feed(models.Model):
    name = models.CharField()
    url = models.CharField()