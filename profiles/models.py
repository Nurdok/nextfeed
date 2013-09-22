from django.db import models
from django.contrib.auth.models import User
from randomslug.models import RandomSlugField

from feeds.models import Entry, Feed


class UserProfile(models.Model):
    user = models.ForeignKey(User)
    feeds = models.ManyToManyField(to=Feed, through='profiles.Subscription')
    entries = models.ManyToManyField(to=Entry,
                                     through='profiles.UserEntryDetail')
    next_slug = RandomSlugField(slug_length=10)

    def __unicode__(self):
        return u"{}'s profile".format(self.user.username)


class UserEntryDetail(models.Model):
    profile = models.ForeignKey(to=UserProfile)
    entry = models.ForeignKey(to=Entry)
    read = models.BooleanField()

    def __unicode__(self):
        return u'User: {}, Entry: {}, Read: {}'.format(
                                                self.profile.user.username,
                                                self.entry,
                                                self.read)


class Subscription(models.Model):
    profile = models.ForeignKey(to=UserProfile)
    feed = models.ForeignKey(to=Feed)

    def unread_entries_num(self):
        unread_entries = UserEntryDetail.objects.filter(read=False,
                                                        profile=self.profile,
                                                        entry__feed=self.feed)
        return unread_entries.count()



