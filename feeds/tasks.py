import time
import feedparser
from celery import task
from feeds.models import Feed, Entry
from django.core.exceptions import ObjectDoesNotExist
from profiles.models import UserProfile, UserEntryDetail


def poll_feed(feed):
    parser = feedparser.parse(feed.link)

    # Add entries from feed
    entries = parser.entries
    for entry in entries:
        try:
            Entry.objects.get(link=entry.link)
        except ObjectDoesNotExist:
            pass
        else:
            continue

        published = time.strftime('%Y-%m-%d %H:%M', entry.published_parsed)
        entry_obj = Entry(feed=feed,
                          title=entry.title,
                          link=entry.link,
                          published=published)
        entry_obj.save()

        subscribers = UserProfile.objects.filter(feeds__in=feed)
        for profile in subscribers:
            UserEntryDetail(entry=entry_obj,
                            profile=profile,
                            read=False).save()


@task
def poll_all_feeds():
    feeds = Feed.objects.all()
    for feed in feeds:
        poll_feed(feed)
