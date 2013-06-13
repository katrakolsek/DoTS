from django.conf.urls import patterns, include, url
from DoTS.views import home, prediction, receptors, receptor, about, docking, converter
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'DoTS.views.home', name='home'),
    url(r'^prediction', prediction),
    url(r'^docking/(\d+)/$', docking),
    url(r'^receptors', receptors),
    url(r'^receptor/(\d+)/$', receptor),
    url(r'^about', about),
    url(r'^converter', converter),
    # url(r'^DoTS/', include('DoTS.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
