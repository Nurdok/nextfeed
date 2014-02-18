"""Feed-related tests."""

import mock
import datetime
from collections import namedtuple
from django.test import TestCase
from django.contrib.auth.models import User

from feeds import tasks
from feeds.models import Feed, Entry
from profiles.models import UserEntryDetail, UserProfile, Subscription

FeedParserEntry = namedtuple('FeedParserEntry', 'link title published_parsed')


class PollFeedTest(TestCase):
    def setUp(self):
        self.feed = Feed(link="http://link.to/rss.xml",
                         title="A Feed")
        self.feed.save()

        # Create an entry
        published = datetime.datetime(2013, 9, 25, 4, 0)
        published = published.timetuple()
        self.entry1 = FeedParserEntry(title="An Entry",
                                      link="http://entry",
                                      published_parsed=published)

        # Create another entry
        published = datetime.datetime(2013, 9, 28, 4, 0)
        published = published.timetuple()
        self.entry2 = FeedParserEntry(title="Another Entry",
                                      link="http://another/entry",
                                      published_parsed=published)

        # Create users
        user1 = User(username="user1")
        user1.save()
        self.profile1 = UserProfile(user=user1)
        self.profile1.save()

        user2 = User(username="user2")
        user2.save()
        self.profile2 = UserProfile(user=user2)
        self.profile2.save()

    def test_profile_display(self):
        self.assertEqual(str(self.profile1), "user1's profile")
        self.assertEqual(str(self.profile2), "user2's profile")

    @mock.patch('feedparser.parse')
    def test_poll_new_subscriber(self, mock_parse):
        """Test a successful polling of a feed."""
        
        # Set up mock data
        parser = mock.MagicMock()
        parser.entries = [self.entry1, self.entry2]
        mock_parse.return_value = parser
        Subscription(profile=self.profile1, feed=self.feed).save()
        
        # Verify initial state
        self.assertEqual(Feed.objects.count(), 1)
        self.assertEqual(Entry.objects.count(), 0)
        self.assertEqual(UserEntryDetail.objects.count(), 0)

        # Perform poll
        tasks.poll_feed(self.feed)
        
        # Verify final state
        self.assertEqual(Feed.objects.count(), 1)
        self.assertEqual(Entry.objects.count(), 2)
        self.assertEqual(UserEntryDetail.objects.count(), 2)

    @mock.patch('feedparser.parse')
    def test_poll_two_new_subscribers(self, mock_parse):
        """Test a successful polling of a feed."""

        # Set up mock data
        parser = mock.MagicMock()
        parser.entries = [self.entry1, self.entry2]
        mock_parse.return_value = parser
        Subscription(profile=self.profile1, feed=self.feed).save()
        Subscription(profile=self.profile2, feed=self.feed).save()

        # Verify initial state
        self.assertEqual(Feed.objects.count(), 1)
        self.assertEqual(Entry.objects.count(), 0)
        self.assertEqual(UserEntryDetail.objects.count(), 0)

        # Perform poll
        tasks.poll_feed(self.feed)

        # Verify final state
        self.assertEqual(Feed.objects.count(), 1)
        self.assertEqual(Entry.objects.count(), 2)
        self.assertEqual(UserEntryDetail.objects.count(), 4)

    @mock.patch('feedparser.parse')
    def test_poll_new_and_existing_subscribers(self, mock_parse):
        """Test a successful polling of a feed."""

        # Set up mock data
        parser = mock.MagicMock()
        parser.entries = [self.entry1, self.entry2]
        mock_parse.return_value = parser
        Subscription(profile=self.profile1, feed=self.feed).save()
        Subscription(profile=self.profile2, feed=self.feed).save()
        entry1 = Entry(link=self.entry1.link,
                       feed=self.feed,
                       title=self.entry1.title,
                       published=datetime.datetime(2013, 9, 25, 4, 0))
        entry1.save()
        UserEntryDetail(profile=self.profile1, entry=entry1).save()

        # Verify initial state
        self.assertEqual(Feed.objects.count(), 1)
        self.assertEqual(Entry.objects.count(), 1)
        self.assertEqual(UserEntryDetail.objects.count(), 1)

        # Perform poll
        tasks.poll_feed(self.feed)

        # Verify final state
        self.assertEqual(Feed.objects.count(), 1)
        self.assertEqual(Entry.objects.count(), 2)
        self.assertEqual(UserEntryDetail.objects.count(), 4)

    @mock.patch('feedparser.parse')
    def test_poll_after_unsubscribe(self, mock_parse):
        # Set up mock data
        parser = mock.MagicMock()
        parser.entries = [self.entry1]
        mock_parse.return_value = parser
        Subscription(profile=self.profile1, feed=self.feed).save()

        # Verify initial state
        self.assertEqual(Feed.objects.count(), 1)
        self.assertEqual(Entry.objects.count(), 0)
        self.assertEqual(UserEntryDetail.objects.count(), 0)

        # Perform poll
        tasks.poll_feed(self.feed)

        # Verify state
        self.assertEqual(Feed.objects.count(), 1)
        self.assertEqual(Entry.objects.count(), 1)
        self.assertEqual(UserEntryDetail.objects.count(), 1)

        # Unsubscribe
        self.profile1.unsubscribe(self.feed)

        # Verify state
        self.assertEqual(Feed.objects.count(), 1)
        self.assertEqual(Entry.objects.count(), 1)
        self.assertEqual(UserEntryDetail.objects.count(), 0)

        # Resubscribe
        self.profile1.subscribe(self.feed)

        # Perform poll (find another entry)
        parser.entries = [self.entry1, self.entry2]
        tasks.poll_feed(self.feed)

        # Verify final state
        self.assertEqual(Feed.objects.count(), 1)
        self.assertEqual(Entry.objects.count(), 2)
        self.assertEqual(UserEntryDetail.objects.count(), 2)

    @mock.patch('feedparser.parse')
    def test_mark_read_unread(self, mock_parse):
        parser = mock.MagicMock()
        parser.entries = [self.entry1, self.entry2]
        mock_parse.return_value = parser

        unread_entries = self.profile1.unread_entries(self.feed)
        self.assertEqual(unread_entries, 0)

        self.profile1.subscribe(self.feed)
        tasks.poll_feed(self.feed)
        unread_entries = self.profile1.unread_entries(self.feed)
        self.assertEqual(unread_entries, 2)

        self.profile1.mark_read(self.feed)
        unread_entries = self.profile1.unread_entries(self.feed)
        self.assertEqual(unread_entries, 0)

        self.profile1.mark_unread(self.feed)
        unread_entries = self.profile1.unread_entries(self.feed)
        self.assertEqual(unread_entries, 2)


