from django.conf.urls.defaults import patterns, include, url
from npg import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'npg.views.home', name='home'),
    # url(r'^npg/', include('npg.foo.urls')),
    (r'^$', include('npg.web.urls')),
    (r'^services/', include('npg.soap.urls')),
    (r'^request/', include('npg.web.urls')),
    (r'^reports/', include('npg.reports.urls')),
	(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                 {'document_root': settings.MEDIA_ROOT}),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
