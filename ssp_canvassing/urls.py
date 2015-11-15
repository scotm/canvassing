from django.conf.urls import patterns, include, url
from django.contrib import admin

from core.views import DomecileMapView, DomecileAddressView, HomepageView, TemplateView


urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'ssp_canvassing.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^$', HomepageView.as_view(), name='homepage'),
                       url(r'^about_rise/$', TemplateView.as_view(template_name='about_rise.html'),
                           name='about_rise'),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^base/', TemplateView.as_view(template_name='base.html')),
                       url(r'^contact/', include('core.urls')),
                       url(r'^', include('leafleting.urls')),
                       url(r'^postcode/', include('postcode_locator.urls')),
                       url(r'reports/', include('reporting.urls')),
                       url(r'', include('campaigns.urls')),
                       url(r'^ajax/get_domeciles$', DomecileMapView.as_view(), name='get_domeciles'),
                       url(r'^ajax/get_addresses$', DomecileAddressView.as_view(), name='get_addresses'),
                       url('^', include('django.contrib.auth.urls')),
                       # url(r'^ward/(?P<slug>[a-z\-_]+)', WardView.as_view()),
                       )
