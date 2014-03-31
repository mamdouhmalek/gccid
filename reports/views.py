from configuration import GetConfig, LogInput
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response


def index(request):
	PageName = "Reports"

	return render_to_response('reports/index.html', {
			'page_name':PageName,
			#'server':GetConfig("SOAP_CONNECTION"),
	})
