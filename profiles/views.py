from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.detail import DetailView
from django.http.response import HttpResponseRedirect
from profiles.models import UserProfile, UserEntryDetail
from django.contrib.auth.models import User
from feeds.forms import FeedForm
import feedparser
from feeds.models import Feed, Entry
from django.views.generic.edit import FormView, DeleteView
from django.core.exceptions import ObjectDoesNotExist
import time
from feeds.tasks import poll_feed


class HomeView(TemplateView):
    template_name = 'home.html'


class AboutView(TemplateView):
    template_name = 'about.html'


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
        print entries.order_by('published')
        entry = entries.order_by('published')[0]
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
        parser = feedparser.parse(link)
        feed = parser.feed
        title = feed.title
        try:
            feed_obj = Feed.objects.get(link=link)
        except ObjectDoesNotExist:
            feed_obj = Feed(link=link, title=title)
            feed_obj.save()
        user.get_profile().feeds.add(feed_obj)
        poll_feed(feed_obj)
        return super(DashboardView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        user = self.request.user
        try:
            user.get_profile()
        except:
            UserProfile(user=user).save()
        return super(DashboardView, self).get_context_data(*args, **kwargs)


class EditEntriesForFeedView(RedirectView):
    url = "/dashboard"
    permanent = False

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        feed_id = self.kwargs['id']
        feed = Feed.objects.get(id=feed_id)
        self.edit_feed(feed)
        entries = UserEntryDetail.objects.filter(profile=user.get_profile(),
                                                 entry__feed=feed)
        for user_entry in entries:
            print user_entry
            self.edit_entry(user_entry)
        return super(EditEntriesForFeedView, self).dispatch(request,
                                                            *args,
                                                            **kwargs)

    def edit_feed(self, feed):
        pass

    def edit_entry(self, entry):
        pass


class DeleteFeedView(EditEntriesForFeedView):
    def edit_feed(self, feed):
        feed.delete()


class MarkUnreadView(EditEntriesForFeedView):
    def edit_entry(self, entry):
        entry.read = False
        entry.save()


class MarkReadView(EditEntriesForFeedView):
    def edit_entry(self, entry):
        entry.read = True
        entry.save()
