from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required


class HomeView(TemplateView):
    template_name = 'home.html'


@login_required
class NextView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        # Here be dragons.
        pass


@login_required
class UserProfileView(DetailView):
    template_name = 'user_profile.html'


class LoginView():
