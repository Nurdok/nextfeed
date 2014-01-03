"""Parse and create OPML files for RSS readers and aggregators."""

import opml


def parse(stream):
    """Parses an OPML string and returns a list of feed URLs.

    :param stream: a string containing the entire opml file.

    """
    pass


def create(feeds):
    """Creates an OPML file from a list of feeds.

    :param feeds: a list of feeds, each should have a 'url' and 'title' attrs.

    """
    pass