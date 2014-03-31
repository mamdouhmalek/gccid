## This is to host the nptypes.xsd file and make it accessible from the web
## Static hosting from the web
from configuration import GetConfig
import os, tempfile, zipfile
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse

def send_file(request):
	"""
	Send a file through Django without loading the whole file into
	memory at once. The FileWrapper will turn the file object into an
	iterator for chunks of 8KB.
	"""
	filename = GetConfig("XSD_LOCATION")
	wrapper = FileWrapper(file(filename))
	response = HttpResponse(wrapper, content_type='text/xml')
	response['Content-Length'] = os.path.getsize(filename)
	return response
