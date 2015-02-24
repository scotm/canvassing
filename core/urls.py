__author__ = 'scotm'
from django.conf.urls import patterns, url
from core.views import ContactView, ContactListView

urlpatterns = patterns('',
                        url(r'^$', ContactListView.as_view()),
                        url(r'^(?P<pk>[0-9]+)', ContactView.as_view()),
)
