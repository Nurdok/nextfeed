from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.detail import DetailView
from django.http.response import HttpResponseRedirect
from profiles.models import UserProfile
from django.contrib.auth.models import User
from feeds.forms import FeedForm
import feedparser
from feeds.models import Feed
from django.views.generic.edit import FormView
from django.core.exceptions import ObjectDoesNotExist


class HomeView(TemplateView):
    template_name = 'home.html'


class NoEntriesView(TemplateView):
    template_name = 'noentries.html'


class NextView(RedirectView):
    permanent = False

    def get_redirect_url(self, **kwargs):
        subscription = self.request.GET['subscription']
        profile = UserProfile.objects.get(next_slug=subscription)
        entries = profile.entries.filter(userentrydetail__read=False)
        if not entries.exists():
            return '/noentries'
        entry = entries.order_by('-published')[0]
        user_entry = entry.userentrydetail_set.get(profile=profile)
        user_entry.read = True
        user_entry.save()
        return entry.link


class DashboardView(FormView):
    template_name = 'dashboard.html'
    form_class = FeedForm
    success_url = '/dashboard'

    def form_valid(self, form):
        user = self.request.user
        link = form.cleaned_data['link']
        feed = feedparser.parse(link).feed
        title = feed.title
        try:
            feed_obj = Feed.objects.get(link=link)
        except ObjectDoesNotExist:
            feed_obj = Feed(link=link, title=title)
            feed_obj.save()
        user.get_profile().feeds.add(feed_obj)
        return super(DashboardView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        user = self.request.user
        try:
            user.get_profile()
        except:
            UserProfile(user=user).save()
        return super(DashboardView, self).get_context_data(*args, **kwargs)
