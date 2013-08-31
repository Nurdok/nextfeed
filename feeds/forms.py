from django.forms.models import ModelForm
from django.forms.widgets import TextInput

import feedparser

from feeds.models import Feed
from django.core.exceptions import ValidationError


class FeedForm(ModelForm):
    class Meta:
        model = Feed
        fields = ['link']
        widgets = {
            'link': TextInput(attrs={'placeholder': 'Paste RSS address here!',
                                     'id': 'feed-url-input'})
        }

    def clean(self):
        cleaned_data = super(FeedForm, self).clean()
        parser = feedparser.parse(cleaned_data.get('link'))
        if parser.feed == {}:
            raise ValidationError("The link provided is not a valid feed.")
        return cleaned_data
