from django.db import models
from django.contrib.auth.models import User
from randomslug.models import RandomSlugField

from feeds.models import Entry, Feed


class UserProfile(models.Model):
    user = models.ForeignKey(User)
    feeds = models.ManyToManyField(to=Feed)
    entries = models.ManyToManyField(to=Entry,
                                     through='profiles.UserEntryDetail')
    next_slug = RandomSlugField(slug_length=10)


class UserEntryDetail(models.Model):
    profile = models.ForeignKey(to=UserProfile)
    entry = models.ForeignKey(to=Entry)
    read = models.BooleanField()
