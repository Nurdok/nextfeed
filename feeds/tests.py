"""Feed-related tests."""

import mock
from collections import namedtuple
from django.test import TestCase

from feeds import tasks
from feeds.models import Feed, Entry
from profiles.models import UserEntryDetail

FeedParserEntry = namedtuple('FeedParserEntry','link title published_parsed')


class PollFeedTest(TestCase):
    def setUp(self):
        self.feed = Feed(link="http://link.to/rss.xml",
                         title="A Feed")
        self.feed.save()
                         
    
    @mock.patch('feedparser.parse')
    def test_successful_poll(self, mock_parser):
        """Test a successful polling of a feed."""
        
        # Set up mock data
        published = ()
        feedparser_entry = FeedParserEntry(title="An Entry",
                                           link="http://entry",
                                           published_parsed=published)
        mock_parser.entries = [feedparser_entry]
        
        # Verify initial state
        self.assertEqual(Feed.objects.count(), 1)
        self.assertEqual(Entry.objects.count(), 0)
        self.assertEqual(UserEntryDetail.objects.count(), 0)
        
        # Perform poll
        tasks.poll_feed(self.feed)
        
        # Verify final state
        self.assertEqual(Feed.objects.count(), 1)
        self.assertEqual(Entry.objects.count(), 1)
        self.assertEqual(UserEntryDetail.objects.count(), 0)
        
        
        