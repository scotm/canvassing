from django.conf.urls import url
from django.views.generic import TemplateView

__author__ = 'scotm'

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="reporting_incomplete.html"), name='reporting'),
]
