import json

from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView, RedirectView, View
from django.views.generic.detail import DetailView
from django.http.response import HttpResponseRedirect, Http404, HttpResponseBadRequest
from profiles.forms import ReportForm
from profiles.models import UserProfile, UserEntryDetail, Subscription
from django.contrib.auth.models import User
from feeds.forms import FeedForm
import feedparser
from feeds.models import Feed, Entry
from django.views.generic.edit import FormView
from django.core.exceptions import ObjectDoesNotExist
import time
from django.http import HttpResponse
from feeds.tasks import poll_feed
from profiles.tasks import report_issue


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
        try:
            profile = UserProfile.objects.get(next_slug=subscription)
        except Exception:
            raise Http404()
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
        if not link.startswith('http://'):
            link = 'http://{}'.format(link)
        parser = feedparser.parse(link)
        feed = parser.feed
        title = feed.title
        try:
            feed_obj = Feed.objects.get(link=link)
        except ObjectDoesNotExist:
            feed_obj = Feed(link=link, title=title)
            feed_obj.save()
        profile = user.get_profile()
        Subscription(profile=profile, feed=feed_obj).save()
        poll_feed(feed_obj)
        return super(DashboardView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        user = self.request.user
        try:
            user.get_profile()
        except:
            UserProfile(user=user).save()
        context = super(DashboardView, self).get_context_data(*args, **kwargs)
        subscriptions = Subscription.objects.filter(profile=user.get_profile())
        context['subscriptions'] = subscriptions
        return context


class EditEntriesForFeedView(RedirectView):
    url = "/dashboard"
    permanent = False

    def _get_feed(self):
        feed_id = self.kwargs['id']
        return Feed.objects.get(id=feed_id)


class UnsubscribeView(EditEntriesForFeedView):
    def dispatch(self, request, *args, **kwargs):
        feed = self._get_feed()
        self.request.user.get_profile().unsubscribe(feed)
        return super(UnsubscribeView, self).dispatch(request, *args, **kwargs)


class MarkUnreadView(EditEntriesForFeedView):
    def dispatch(self, request, *args, **kwargs):
        feed = self._get_feed()
        self.request.user.get_profile().mark_unread(feed)
        return super(MarkUnreadView, self).dispatch(request, *args, **kwargs)


class MarkReadView(EditEntriesForFeedView):
    def dispatch(self, request, *args, **kwargs):
        feed = self._get_feed()
        self.request.user.get_profile().mark_read(feed)
        return super(MarkReadView, self).dispatch(request, *args, **kwargs)


def subscription(request):
    profile = request.user.get_profile()
    if request.method == "GET":
        subscriptions = Subscription.objects.filter(profile=profile)
        subscriptions_json = [{'id': s.feed.id,
                               'title': s.feed.title,
                               'unread_entries': profile.unread_entries(s.feed)}
                              for s in subscriptions]
        return HttpResponse(json.dumps(subscriptions_json),
                            content_type='application/json')
    if request.method == "POST":
        link = json.loads(request.body)['link']
        if not link.startswith('http://'):
            link = 'http://{}'.format(link)
        parser = feedparser.parse(link)
        feed = parser.feed
        try:
            title = feed.title
        except AttributeError:
            return HttpResponseBadRequest('Invalid feed')
        try:
            feed_obj = Feed.objects.get(link=link)
        except ObjectDoesNotExist:
            feed_obj = Feed(link=link, title=title)
            feed_obj.save()
        if Subscription.objects.filter(profile=profile, feed=feed_obj).exists():
            return HttpResponseBadRequest('You are already subscribed to this '
                                          'feed')
        Subscription.objects.get_or_create(profile=profile, feed=feed_obj)
        try:
            poll_feed(feed_obj)
        except AttributeError:
            return HttpResponseBadRequest('Invalid feed')
        return HttpResponse()


class ReportView(TemplateView):

    def post(self, request):
        data = json.loads(request.body)
        report_form = ReportForm({'summary': data[u'summary'],
                                  'details': data[u'details']})
        if report_form.is_valid():
            report_issue(report_form.cleaned_data['summary'],
                         report_form.cleaned_data['details'])
        else:
            return HttpResponseBadRequest('Form was invalid: {}'.format(report_form.errors))
        return HttpResponse("Report was submitted!")
