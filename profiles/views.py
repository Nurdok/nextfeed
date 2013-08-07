from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.detail import DetailView
from django.http.response import HttpResponseRedirect
from profiles.models import UserProfile
from django.contrib.auth.models import User


class HomeView(TemplateView):
    template_name = 'home.html'


class NextView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        # Here be dragons.
        return HttpResponseRedirect('/')


class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, *args, **kwargs):
        user = self.request.user
        try:
            user.get_profile()
        except:
            UserProfile(user=user).save()
        return super(DashboardView, self).get_context_data(*args, **kwargs)
