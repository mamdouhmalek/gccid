from configuration import GetConfig, LogInput
from suds.client import Client
from suds.transport.http import HttpAuthenticated
from suds.transport.https import HttpTransport

from urllib2 import HTTPBasicAuthHandler, build_opener, install_opener, urlopen, BaseHandler

import xml
from xml.dom import minidom


if GetConfig('SOAP_CONNECTION') == "LIVE":
	connctions = "CSL"
elif GetConfig('SOAP_CONNECTION') == "TEST":
	connctions = "CST"

userid = GetConfig(connctions).get('user')
passwd = GetConfig(connctions).get('password')
url = GetConfig(connctions).get('url')

######################### Basic Authentication
import base64
class HTTPSudsPreprocessor(BaseHandler):
    def http_request(self, req):
        req.add_header('Content-Type', 'text/xml; charset=utf-8')
        req.add_header('WWW-Authenticate', 'Basic realm="Control Panel"')
        #The below lines are to encode the credentials automatically
        cred=userid+':'+passwd
        if cred!=None:
            enc_cred=base64.encodestring(cred)
            req.add_header('Authorization', 'Basic '+ enc_cred.replace('\012',''))
        return req
    https_request = http_request

http = HttpTransport()
opener = build_opener(HTTPSudsPreprocessor)
http.urlopener = opener


######################### For  Basic Authentication #################################
client = Client(url, location=url.replace('?wsdl',''), transport=http, cache=None, timeout=90, faults=False, retxml=True)
#####################################################################################


def SendSOAPMessage(code, request):
	##LogInput('core_send.py >> Looking for  %s' % request.get('MessageCode'))

    if code == "NpRequest":
    
        try:
			#LogInput('Inside try statement Sending NpRequest!! %s',str(request))

			bb=client.service.SendNpRequest(**request)
			#LogInput('printing client code %s' % str(bb))
			return bb
        except Exception, e:
            #LogInput('failed to send NpRequest because of %s',str(e))
            return False


    elif code == "NpRequestAccept":
		#LogInput('Sending %s' % code)
		return client.service.SendNpRequestAccept(**request)

    elif code == "NpRequestReject":
		#LogInput('Sending %s' % code)
		return client.service.SendNpRequestReject(**request)

    elif code == "NpRequestCancel":
		#LogInput('Sending %s' % code)
		return client.service.SendNpRequestCancel(**request)

    elif code == "NpExecute":
		#LogInput('Sending %s' % code)
		return client.service.SendNpExecute(**request)

    elif code == "NpExecuteComplete":
		#LogInput('Sending %s' % code)
		try:
			#LogInput('Inside try statement !!')
			bb=client.service.SendNpExecuteComplete(**request)
			#LogInput('printing client code %s' % str(bb))
			return bb
		except Exception, e:
			#LogInput('failed to send NpExecuteComplete because of %s',str(e))
			return False

    elif code == "NpDeactivate":
		#LogInput('Sending %s' % code)
		return client.service.SendNpDeactivate(**request)

    elif code == "NpDeactivateComplete":
		#LogInput('Sending %s' % code)
		return client.service.SendNpDeactivateComplete(**request)

    elif code == "NpQuery":
		#LogInput('Sending %s' % code)
		return client.service.SendNpQuery(**request)

    elif code == "NpBillingResolution":
		#LogInput('Sending %s' % code)
		return client.service.SendNpBillingResolution(**request)

    elif code == "NpBillingResolutionReceived":
		#LogInput('Sending %s' % code)
		return client.service.SendNpBillingResolutionReceived(**request)

    elif code == "NpBillingResolutionEnd":
		#LogInput('Sending %s' % code)
		return client.service.SendNpBillingResolutionEnd(**request)

    elif code == "NpBillingResolutionAlert":
		#LogInput('Sending %s' % code)
		return client.service.SendNpBillingResolutionAlert(**request)

    elif code == "NpBillingResolutionAlertReceived":
		#LogInput('Sending %s' % code)
		return client.service.SendNpBillingResolutionAlertReceived(**request)

    #else: return 'Bad Message or request string'

def myparser(InString):


	if isinstance(InString,tuple):
		#res[0] is the error code 500 due to non correct input
		#res[1] is containg all the parameters
		g=[i for i in InString[1]]
		#g[0][0] is an ErrorNotification string, it's not the message code
		d=g[0][1]
		#convert the resulting content to a dictionary
		Dict=dict(d)
		#We need to define some exception to raise an error
		return Dict

	if isinstance(InString,str):
		res=str(InString)
        #print res
        convert=minidom.parseString(res)

        Dict={}
        flag=0
        n='npc:'
        c='com:'
        Marray=['ServiceType','MessageCode','PortID','OriginationID','DestinationID']
        for m in Marray:
			try:
				Dict[m]=convert.getElementsByTagName(c+m)[0].firstChild.data
				flag=1
			except:
				try:
					Dict[m]=convert.getElementsByTagName(n+m)[0].firstChild.data
					flag=2
				except:
					#make some logging
					#LogInput('Cannot parse the XML in myparser function')
					return False


        if flag==1:
			h=c
        elif flag==2:
			h=n
        else:
			#LogInput('Un known XML Tag name !!!')
			return False

        if convert.getElementsByTagName(h+'MessageCode')[0].firstChild.data=='NpRequestAck':
			params=['Number','SubmissionID','DonorID','RecipientID']
			for m in params:
				Dict[m]=convert.getElementsByTagName(h+m)[0].firstChild.data


        if convert.getElementsByTagName(h+'MessageCode')[0].firstChild.data == u"NpDeactivateAck":
			params=['Number','SubscriptionNetworkID','BlockID']
			for m in params:
				Dict[m]=convert.getElementsByTagName(h+m)[0].firstChild.data

        return Dict
