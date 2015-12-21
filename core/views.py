from braces.views import LoginRequiredMixin
from braces.views._access import AccessMixin
from django.conf import settings
from django.views.generic import DetailView, ListView, TemplateView

from core.models import Contact


class CustomLoginRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated() or settings.ALL_ALLOWED:
            return super(CustomLoginRequiredMixin, self).dispatch(request, *args, **kwargs)
        return self.handle_no_permission(request)


class ContactView(LoginRequiredMixin, DetailView):
    model = Contact


class ContactListView(LoginRequiredMixin, ListView):
    model = Contact
    paginate_by = 100


class HomepageView(CustomLoginRequiredMixin, TemplateView):
    template_name = 'homepage.html'

    def get_context_data(self, **kwargs):
        from campaigns.models import Campaign
        kwargs['current_campaign'] = Campaign.get_latest_top_level_campaign()
        return super(HomepageView, self).get_context_data(**kwargs)


class LoginTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'why_canvass.html'
