from django.conf.urls.defaults import patterns, include, url
from django.views.generic import DetailView, ListView
from configuration import GetConfig, LogInput

urlpatterns = patterns('',
	url(r'^$', "reports.views.index"),
	url(r'^new/$', "reports.views.index"),
)

