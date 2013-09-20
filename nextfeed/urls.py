from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from profiles.views import (NextView, DashboardView, HomeView, NoEntriesView,
                            AboutView)
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view()),
    url(r'^openid/?', include('django_openid_auth.urls')),
    url(r'^admin/?', include(admin.site.urls)),
    url(r'^next/?', login_required(NextView.as_view())),
    url(r'^dashboard/?', login_required(DashboardView.as_view())),
    url(r'^noentries/?', NoEntriesView.as_view()),
    url(r'^about$', AboutView.as_view()),
)
