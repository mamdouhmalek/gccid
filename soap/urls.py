from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
	url(r'^NpcdbService$', "soap.views.dispatch"),
	url(r'^nptypes.xsd$', "soap.expose_xsd.send_file"),
	url(r'^NpcdbService/nptypes.xsd$', "soap.expose_xsd.send_file"),
)

