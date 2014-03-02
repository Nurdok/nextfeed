from django.core.exceptions import MultipleObjectsReturned
import feedparser
from time import mktime
from datetime import datetime
from celery import task
from feeds.models import Feed, Entry
from profiles.models import UserProfile, UserEntryDetail


def poll_feed(feed):
    """Poll entries from a feed."""
    parser = feedparser.parse(feed.link)

    # Add entries from feed
    entries = parser.entries
    for entry in entries:
        try:
            published_parsed = entry.published_parsed
        except AttributeError:  # an Atom feed
            published_parsed = entry.updated_parsed
        published = datetime.fromtimestamp(mktime(published_parsed))
        try:
            entry_obj, _ = Entry.objects.get_or_create(feed=feed,
                                                       title=entry.title,
                                                       link=entry.link,
                                                       published=published)
        except MultipleObjectsReturned:
            pass

        subscribers = UserProfile.objects.filter(feeds=feed)
        for profile in subscribers:
            if not UserEntryDetail.objects.filter(entry=entry_obj,
                                                  profile=profile)\
                                          .exists():
                UserEntryDetail(entry=entry_obj,
                                profile=profile,
                                read=False).save()


@task
def poll_all_feeds():
    feeds = Feed.objects.all()
    for feed in feeds:
        poll_feed(feed)
