from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from profiles.views import NextView, DashboardView, HomeView
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', HomeView.as_view()),
    url(r'^openid/?', include('django_openid_auth.urls')),
    url(r'^admin/?', include(admin.site.urls)),
    url(r'^next/?', login_required(NextView.as_view())),
    url(r'^dashboard/?', login_required(DashboardView.as_view())),
    # url(r'^nextfeed/', include('nextfeed.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
)
