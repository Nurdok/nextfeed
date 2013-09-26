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

    def subscribe(self, feed):
        Subscription(profile=self, feed=feed).save()

    def unsubscribe(self, feed):
        Subscription.objects.get(profile=self, feed=feed).delete()
        self._get_entries(feed).delete()

    def mark_read(self, feed):
        entries = self._get_entries(feed)
        for entry in entries:
            entry.read = True
            entry.save()

    def mark_unread(self, feed):
        entries = self._get_entries(feed)
        for entry in entries:
            entry.read = False
            entry.save()

    def _get_entries(self, feed):
        return UserEntryDetail.objects.filter(profile=self, entry__feed=feed)


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



