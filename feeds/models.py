from django.db import models


class Feed(models.Model):
    url = models.CharField(max_length=1000)


class Entry(models.Model):
    url = models.CharField(max_length=1000)
    feed = models.ForeignKey(to=Feed)
