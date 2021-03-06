from django.db import models


class Feed(models.Model):
    title = models.CharField(max_length=200)
    link = models.CharField(max_length=1000)

    def __unicode__(self):
        return self.title


class Entry(models.Model):
    title = models.CharField(max_length=200)
    link = models.CharField(max_length=1000)
    feed = models.ForeignKey(to=Feed)
    published = models.DateTimeField()

    def __unicode__(self):
        return u'{}: {}'.format(self.feed, self.title)
