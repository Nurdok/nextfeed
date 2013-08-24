from django.forms.models import ModelForm
from feeds.models import Feed
from django.forms.widgets import TextInput


class FeedForm(ModelForm):
    class Meta:
        model = Feed
        fields = ['link']
        widgets = {
            'link': TextInput(attrs={'placeholder': 'Paste RSS address here!',
                                     'id': 'feed-url-input'})
        }
