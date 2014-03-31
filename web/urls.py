from django.conf.urls.defaults import patterns, include, url
from django.views.generic import DetailView, ListView
from configuration import GetConfig, LogInput

from models import NpMessages, Number_Portability

urlpatterns = patterns('',
	url(r'^$', "web.views.SearchMessages"),
	#url(r'^contact$', "form.views.contact"),
	url(r'^new/$', "web.views.SendNpRequest"),
	url(r'^accept/$', "web.views.SendNpRequestAccept"),
	url(r'^cancel/$', "web.views.SendNpRequestCancel"),
	url(r'^reject/$', "web.views.SendNpRequestReject"),
	url(r'^alld/$', "web.views.AllMessages"),
	url(r'^search/$', "web.views.SearchMessages"),
	url(r'^search/(?P<pk>\d+)$',
		DetailView.as_view(
			model=NpMessages,
			context_object_name='message_list',
			template_name='web/detail.html')),
	url(r'^outgoing/$', "web.views.SentRequest"),
	url(r'^incoming/$', "web.views.ReceivedRequest"),
   '''
	url(r'^outgoing/$',
		ListView.as_view(
			queryset=NpMessages.objects.filter(direction="OUT",message_code="NpRequest",new_message_unread="Y"),
			context_object_name='message_list',
			#server=GetConfig("SOAP_CONNECTION"),
			template_name='web/OutgoingRequests.html')),
	url(r'^incoming/$',
		ListView.as_view(
			queryset=NpMessages.objects.filter(direction="IN",message_code="NpRequest",new_message_unread="Y"),
			context_object_name='message_list',
			#server=GetConfig("SOAP_CONNECTION"),
			template_name='web/IncomingRequests.html')),
	url(r'^all/$',
		ListView.as_view(
			queryset=NpMessages.objects.order_by('-message_id')[:50],
			context_object_name='message_list',
			template_name='web/AllMessages.html')),
	
	url(r'^lightspeed/$',
		ListView.as_view(
			queryset = Number_Portability.objects.using('lightspeed').all(),
			context_object_name='message_list',
			template_name='web/lightspeed.html')),
	'''
	
)

