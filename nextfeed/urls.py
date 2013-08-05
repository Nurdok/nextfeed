from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from profiles.views import NextView, UserProfileView, LoginView, HomeView
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', HomeView.as_view()),
    url(r'^login/?', LoginView.as_view())
    url(r'^$/(?P<user>\w+)/next/?', NextView.as_view()),
    url(r'^$/(?P<user>\w+)/?', UserProfileView.as_view()),
    # url(r'^nextfeed/', include('nextfeed.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
