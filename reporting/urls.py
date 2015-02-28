__author__ = 'scotm'
from django.views.generic import TemplateView
from django.conf.urls import patterns, url


urlpatterns = patterns('',
                       url(r'^$', TemplateView.as_view(template_name="reporting_incomplete.html"), name='reporting'),
)
