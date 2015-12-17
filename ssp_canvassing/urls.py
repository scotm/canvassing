from django.conf.urls import include, url
from django.contrib import admin

from core.views import DomecileAddressView, HomepageView, TemplateView

urlpatterns = [
    url(r'^$', HomepageView.as_view(), name='homepage'),
    url(r'^about_the_ssp/$', TemplateView.as_view(template_name='about_the_ssp.html'),
        name='about_the_ssp'),
    url(r'bugs_and_features', TemplateView.as_view(template_name='bugs.html'), name='bugs'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^base/', TemplateView.as_view(template_name='base.html')),
    url(r'^contact/', include('core.urls')),
    url(r'^', include('leafleting.urls')),
    url(r'^', include('polling.urls')),
    url(r'^postcode/', include('postcode_locator.urls')),
    url(r'reports/', include('reporting.urls')),
    url(r'', include('campaigns.urls')),
    url(r'^ajax/get_domeciles$', 'core.views.domecile_map_view', name='get_domeciles'),
    url(r'^ajax/get_addresses$', DomecileAddressView.as_view(), name='get_addresses'),

    url('^', include('django.contrib.auth.urls')),
    # url(r'^ward/(?P<slug>[a-z\-_]+)', WardView.as_view()),
]
