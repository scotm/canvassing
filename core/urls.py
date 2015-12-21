from django.conf.urls import url

from core.views import ContactView, ContactListView

__author__ = 'scotm'

urlpatterns = [
    url(r'^$', ContactListView.as_view(), name='contact_list'),
    url(r'^(?P<pk>[0-9]+)', ContactView.as_view(), name='contact_view'),
]
