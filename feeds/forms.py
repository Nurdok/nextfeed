from django.forms.models import ModelForm
from feeds.models import Feed


class FeedForm(ModelForm):
    class Meta:
        model = Feed
        fields = ['link']
