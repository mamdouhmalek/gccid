# Create your views here.
from configuration import GetConfig, LogInput
from django.http import HttpResponse, HttpResponseRedirect
import datetime
from django import forms
from django.shortcuts import render_to_response
from models import NpMessages, Number_Portability
from models import NpMessagesForm
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import loader, Context
from django.db.models import Q

#Importing the sender fucntion that will take data from from and pass it to CS
from soap.sendsoap import send_parse_save

cs_ret=""

		
def index(request):
	return render_to_response('web/index.html')

def SentRequest(request):
	PageName = "Sent Request"
	
	queryset = NpMessages.objects.filter(direction="OUT",message_code="NpRequest",new_message_unread="Y")

	return render_to_response('web/OutgoingRequests.html', {
			#'form': form,
			'message_list': queryset,
			#'submitted': 'yes',
			#'port_id_list': ShowPortIDList,
			#'related': related,
			#'page_list': PagesList,
			#'current_page': page,
			#'total_results_found': TotalSearchResults,
			'page_name':PageName,
			'server':GetConfig("SOAP_CONNECTION"),
	})

def ReceivedRequest(request):
	PageName = "Received Request"
	
	queryset = NpMessages.objects.filter(direction="IN",message_code="NpRequest",new_message_unread="Y")

	return render_to_response('web/IncomingRequests.html', {
			#'form': form,
			'message_list': queryset,
			#'submitted': 'yes',
			#'port_id_list': ShowPortIDList,
			#'related': related,
			#'page_list': PagesList,
			#'current_page': page,
			#'total_results_found': TotalSearchResults,
			'page_name':PageName,
			'server':GetConfig("SOAP_CONNECTION"),
	})

def AllMessages(request):
	results = ""
	'''
	NpMessages1 = NpMessages.objects.get(message_id='14')
	#LogInput('___________________________  Updating Customer DB %s  ___________________________' % NpMessages1.message_code)
	from soap.voicegateway_update import UpdateVoiceGateway
	results = UpdateVoiceGateway('39003081', 'b04')
	#LogInput('___________________________  End of Updating Customer DB %s  ___________________________' % NpMessages1.message_code)
	'''
	
	'''
	# Delete all the extra NpExecuteComplete outgoing was created in database
	NpMessages1 = NpMessages.objects.filter(message_code = 'NpExecuteComplete', port_id = None).delete()
	'''
	
	'''
	
	## sending email function
	from soap.sendemail import send_email_now
	
	NpMessages1 = NpMessages.objects.get(message_id='7')
	
	message = {
		'time_stamp':NpMessages1.time_stamp,
		'message_id':NpMessages1.message_id,
		'message_code':NpMessages1.message_code,
		'port_id':NpMessages1.port_id,
		'number':NpMessages1.number,
		'service_type':NpMessages1.service_type,
		'donor_id':NpMessages1.donor_id,
		'recipient_id':NpMessages1.recipient_id,
		'origination_id':NpMessages1.origination_id,
		'destination_id':NpMessages1.destination_id,
		'subscription_network_id':NpMessages1.subscription_network_id,
		'block_id':NpMessages1.block_id,
		'submission_id':NpMessages1.submission_id,
		'sim_card_number':NpMessages1.sim_card_number,
		'company_flag':NpMessages1.company_flag,
		'commercial_reg_number':NpMessages1.commercial_reg_number,
		'passport_number':NpMessages1.passport_number,
		'cpr':NpMessages1.cpr,
		'reject_code':NpMessages1.reject_code,
		'new_route':NpMessages1.new_route,
		'porting_date_time':NpMessages1.porting_date_time,
		'error_code':NpMessages1.error_code,
		'rejected_message_code':NpMessages1.rejected_message_code,
		'comments':NpMessages1.comments,
		'direction':NpMessages1.direction,
		'new_message_unread':NpMessages1.new_message_unread,
		} 

	results = send_email_now(NpMessages1)
	'''
	
	
	'''
	## working to show all message grouped by related_message_id
	i = 100000001
	
	NpMessages1 = NpMessages.objects.all()

	NpMessagesDict = {}
	for npm in NpMessages1:
	
		NpMessages2 = NpMessages.objects.filter(related_message_id=str(i))

		NpMessagesFilterd = {}
		for message in NpMessages2:
		NpMessagesFilterd[message.message_id] = message
		
		NpMessagesDict[str(i)] = NpMessagesFilterd
		i += 1
	'''
	''' 
	# not working
	NpMessagesDict={}
	NpMessages1 = NpMessages.objects.all()
	for item in NpMessages1:
		db_dict={
		'time_stamp':item.time_stamp,
		'message_code':item.message_code,
		'port_id':item.port_id,
		'number':item.number,
		'service_type':item.service_type,
		'donor_id':item.donor_id,
		'recipient_id':item.recipient_id,
		'origination_id':item.origination_id,
		'destination_id':item.destination_id,
		'subscription_network_id':item.subscription_network_id,
		'block_id':item.block_id,
		'submission_id':item.submission_id,
		'sim_card_number':item.sim_card_number,
		'company_flag':item.company_flag,
		'commercial_reg_number':item.commercial_reg_number,
		'passport_number':item.passport_number,
		'cpr':item.cpr,
		'reject_code':item.reject_code,
		'new_route':item.new_route,
		'porting_date_time':item.porting_date_time,
		'error_code':item.error_codeerror_code,
		'rejected_message_code':item.rejected_message_code,
		'comments':item.comments,
		'direction':item.direction,
		'new_message_unread':item.new_message_unread,
		} 
		
		NpMessagesDict[item.related_message_id][item.message_id] = db_dict
	'''
		
	'''
	## Rest all related_message_id to None
	NpMessages1 = NpMessages.objects.all()
	
	for item in NpMessages1:
		item.related_message_id = None
		item.save()
	##
	
	i = 100000001
	
	## Fix all related_message_id
	for item in NpMessages1:
		NpMessages2 = NpMessages.objects.filter(related_message_id = None)
		for item in NpMessages2:
		LogInput('inside for 1')
		if item.related_message_id is None and item.port_id is not None:
			LogInput('inside if')
			
			NpMessages2 = NpMessages.objects.filter(port_id = item.port_id)
			LogInput('i = %s' % str(i))

			for item1 in NpMessages2:
				LogInput('inside for 2')
				LogInput('updating = %s' % str(item1.message_id))
				item1.related_message_id = i
				item1.save()
		
			i += 1
			break
	'''
	'''
	## update NpRequest sent out that doesn't have port_id with the right related_message_id
	NpRequest = NpMessages.objects.filter(message_code ="NpRequest", port_id="")
	for item in NpRequest:
		NpRequestAck = NpMessages.objects.get(message_code ="NpRequestAck", submission_id = item.submission_id, number = item.number)
		item.related_message_id = NpRequestAck.related_message_id
		item.save()
	'''
	
	
	return render_to_response('web/AllMessagesR.html', {
		'message_list': results,
		'page_name':PageName,
		'server':GetConfig("SOAP_CONNECTION"),
		}
	)

def SearchMessages(request):
	PageName = "Search Messages"
	#ip_address = request.META.get('HTTP_X_FORWARDED_FOR', '') or request.META.get('REMOTE_ADDR')
	#LogInput('Accessed by: %s' % ip_address)

	if request.method == 'POST': # If the form has been submitted
		#LogInput('Form has been submitted')
		instance = NpMessages()
		#form = NpMessagesForm(request.POST,instance=instance) # A form bound to the POST data
		form = NpMessagesForm(request.POST) # A form bound to the POST data
		#form=form_construct.save(commit=False)
		#if form.is_valid(): # All validation rules pass
		#LogInput('Checking submission')

		#Process the data in form.cleaned_data
		message_code = request.POST['message_code']
		number = str(request.POST['number'])
		port_id = request.POST['port_id']
		#donor_id = request.POST['donor_id']
		#sim_card_number = form.cleaned_data['sim_card_number']
		#company_flag = form.cleaned_data['company_flag']
		#cpr = form.cleaned_data['cpr']
		direction = request.POST['direction']
		
		try:
			related = request.POST['related']
		except:
			related = request.POST['related'] = "NO"
		#comments = form.cleaned_data['comments']

		SearchResults = NpMessages.objects.all()
		
		ShowPortIDList = None
		
		# remove ack messages
		try:
			showAck = request.POST['showAck']
		except:
			showAck = request.POST['showAck'] = "NO"

		if showAck == "NO":
			SearchResults = SearchResults.filter(~Q(message_code__contains = 'Ack'))
		
		if related == "YES" and number != "" and number is not None and port_id == "":
			RelatedSearchResults = SearchResults.filter(number = number)

			RelatedList = []

			for relatedSR in RelatedSearchResults:
				RelatedList.append(relatedSR.port_id)
			
			# remove duplicate port id list
			RelatedList = list(set(RelatedList))
			
			# Remove blank from port id list
			[x for x in RelatedList if x]
			
			RelatedListCount = len(RelatedList)
			
			if RelatedListCount == 1:
				port_id = request.POST['port_id'] = RelatedList[0]
			else:
				ShowPortIDList = RelatedList
		
		if port_id != "" and port_id is not None:
			SearchResults = SearchResults.filter(port_id__contains = port_id)

		if number != "" and number is not None and related == "NO":
			SearchResults = SearchResults.filter(number__contains = number)

		if message_code != "ALL":
			SearchResults = SearchResults.filter(message_code = message_code)

		if direction != "ALL":
			SearchResults = SearchResults.filter(direction = direction)
		
		SearchResults = SearchResults.order_by('-message_id')
		
		if 'ExportReportCSV' in request.POST:
			return ExportCSV(SearchResults)

		if 'ExportReportExcel' in request.POST:
			return ExportExcel(SearchResults)
		
		# This is for Next and Previous 
		paginator = Paginator(SearchResults, 25)
		
		# Count total pages
		TotalPages = paginator.num_pages
		TotalSearchResults = paginator.count
		PagesList = []

		for x in range(TotalPages):
			PagesList.append(x+1)
		
		LogInput('page list: %s' % PagesList)
		
		if 'PageChangeN' in request.POST:
			page = request.POST['pageN']
		elif 'PageChangeP' in request.POST:
			page = request.POST['pageP']
		else:
			page = ""
		
		try:
			SearchResults = paginator.page(page)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			SearchResults = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			SearchResults = paginator.page(paginator.num_pages)
				
		return render_to_response('web/SearchMessages.html', {
			'form': form,
			'message_list': SearchResults,
			'submitted': 'yes',
			'port_id_list': ShowPortIDList,
			'related': related,
			'showAck': showAck,
			'page_list': PagesList,
			'current_page': page,
			'total_results_found': TotalSearchResults,
			'page_name':PageName,
			'server':GetConfig("SOAP_CONNECTION"),
			}
		)
		#else:
		#LogInput('Submission is not Valid')
		#form = NpMessagesForm(request.POST, instance=instance)
	else:
		form = NpMessagesForm()
		submitted = "no"
		#LogInput('New Form is created, ready to be filled and submitted')

	return render_to_response('web/SearchMessages.html', {
		'form': form,
		'page_name':PageName,
		'server':GetConfig("SOAP_CONNECTION"),
		#'total_pages': TotalPages, 
		#'page_list': PagesList,
		}
	)

def ExportExcel(request):
	response = HttpResponse(request, mimetype='application/vnd.ms-excel')
	response = render_to_response("export/ExportSearchExcel.html", {'data': request})
	filename = "MD_Search_Results.xls"
	response['Content-Disposition'] = 'attachment; filename=' + filename
	response['Content-Type'] = 'application/vnd.ms-excel; charset=utf-16'
	return response

def ExportCSV(request):
	# Create the HttpResponse object with the appropriate CSV header.
	response = HttpResponse(mimetype='text/csv')
	filename = "MD_Search_Results.csv"
	response['Content-Disposition'] = 'attachment; filename=' + filename

	t = loader.get_template('export/ExportSearch.txt')
	c = Context({
		'data': request,
		})
	response.write(t.render(c))
	return response


def SendNpRequestReject(request):
	PageName = "Received Request"
	#LogInput('______________________________________________________')
	#LogInput('New Request Cancel')
	if request.method == 'POST': # If the form has been submitted
		#LogInput('Form has been submitted')
		form = NpMessagesForm(request.POST) # A form bound to the POST data
		#LogInput('Checking submission')

		#Process the data in form.cleaned_data
		#those are values from form
		message_id = request.POST['message_id']
		reject_code = request.POST['reject_code']
		comments = request.POST['comments']
		#LogInput('got message id [message_id=%s; reject_code=%s; comments=%s]' % (message_id,reject_code,comments))
		
		#get the request from data base
		NpRequestEntry = NpMessages.objects.get(pk=message_id)

		LogInput('Found Message: %s[ServiceType=%s; MessageCode=%s; Number=%s; PortID=%s; DonorID=%s; RecipientID=%s; OriginationID=%s; DestinationID=%s], DB[MessageID=%s; Time=%s; Direction=%s; New=%s]' % (NpRequestEntry.message_code, NpRequestEntry.service_type, NpRequestEntry.message_code, NpRequestEntry.number, NpRequestEntry.port_id, NpRequestEntry.donor_id, NpRequestEntry.recipient_id, NpRequestEntry.origination_id, NpRequestEntry.destination_id, NpRequestEntry.message_id, NpRequestEntry.time_stamp, NpRequestEntry.direction, NpRequestEntry.new_message_unread))

		NpRequestReject_dict=dict(
			ServiceType = str(NpRequestEntry.service_type) if NpRequestEntry.service_type is not None else str(''),
			MessageCode = str("NpRequestReject"),
			Number = str(NpRequestEntry.number) if NpRequestEntry.number is not None else str(''),
			PortID = str(NpRequestEntry.port_id) if NpRequestEntry.port_id is not None else str(''),
			SubmissionID = str(NpRequestEntry.submission_id) if NpRequestEntry.submission_id is not None else str(''),
			DonorID = str(NpRequestEntry.donor_id) if NpRequestEntry.donor_id is not None else str(''),
			RejectCode = str(reject_code) if reject_code is not None else str(''),
			Comments = str(comments) if comments is not None else str(''),
			RecipientID = str(NpRequestEntry.recipient_id) if NpRequestEntry.recipient_id is not None else str(''),
			OriginationID = GetConfig("ORIGINATION_ID"),
			DestinationID = GetConfig("DESTINATION_ID"),
		)

		#deleting the empty elements from the NpRequest_dict
		for i in NpRequestReject_dict.keys():
			if NpRequestReject_dict[i]=='': NpRequestReject_dict.pop(i)

		#LogInput('Creating NpRequestReject')
		#LogInput('Message%s' % str(NpRequestReject_dict))

		## Added by Hazim to set the fixed fields then store all the message to database
		instance = form.save(commit=False)
		instance.service_type = NpRequestReject_dict.get('ServiceType')
		instance.message_code = NpRequestReject_dict.get('MessageCode')
		instance.number = NpRequestReject_dict.get('Number')
		instance.port_id = NpRequestReject_dict.get('PortID')
		instance.submission_id = NpRequestReject_dict.get('SubmissionID')
		instance.donor_id = NpRequestReject_dict.get('DonorID')
		instance.reject_code = NpRequestReject_dict.get('RejectCode')
		instance.comments = NpRequestReject_dict.get('Comments')
		instance.recipient_id =  NpRequestReject_dict.get('RecipientID')
		instance.origination_id =  NpRequestReject_dict.get('OriginationID')
		instance.destination_id =  NpRequestReject_dict.get('DestinationID')
		instance.direction = "OUT"
		instance.new_message_unread = "N"
		instance.save()
		
		# Send Message and get reply
		global cs_ret
		cs_ret = send_parse_save(NpRequestReject_dict.get('MessageCode'),NpRequestReject_dict)
		
		#LogInput('Message Sent ...')
		
		# update nprequest to read
		NpRequestEntry.new_message_unread = 'N'
		NpRequestEntry.save()

		LogInput('Updated Message: %s[ServiceType=%s; MessageCode=%s; Number=%s; PortID=%s; DonorID=%s; RecipientID=%s; OriginationID=%s; DestinationID=%s], DB[MessageID=%s; Time=%s; Direction=%s; New=%s]' % (NpRequestEntry.message_code, NpRequestEntry.service_type, NpRequestEntry.message_code, NpRequestEntry.number, NpRequestEntry.port_id, NpRequestEntry.donor_id, NpRequestEntry.recipient_id, NpRequestEntry.origination_id, NpRequestEntry.destination_id, NpRequestEntry.message_id, NpRequestEntry.time_stamp, NpRequestEntry.direction, NpRequestEntry.new_message_unread))


		
		queryset = NpMessages.objects.filter(direction="OUT",message_code="NpRequest",new_message_unread="Y")
		
		if cs_ret['MessageCode'] == 'ErrorNotification':
			return render_to_response('web/OutgoingRequests.html', {
				'form': form,
				'reply_list': cs_ret,
				'back_color': "#F78181",
				'message_list': queryset,
				'page_name':PageName,
				'server':GetConfig("SOAP_CONNECTION"),
				})
		else:
			form2 = NpMessagesForm()
			return render_to_response('web/OutgoingRequests.html', {
				'form': form2,
				'reply_list': cs_ret,
				'back_color': "#A9F5A9",
				'message_list': queryset,
				'page_name':PageName,
				'server':GetConfig("SOAP_CONNECTION"),
				})

		
	return HttpResponseRedirect('/request/incoming') # Redirect after POST

def SendNpRequestCancel(request):
	PageName = "Sent Request"
	#LogInput('______________________________________________________')
	#LogInput('New Request Cancel')
	if request.method == 'POST': # If the form has been submitted
		#LogInput('Form has been submitted')
		form = NpMessagesForm(request.POST) # A form bound to the POST data
		#LogInput('Checking submission')

		#Process the data in form.cleaned_data
		#those are values from form
		message_id = request.POST['message_id']
		
		#get the request from data base
		NpRequestEntry = NpMessages.objects.get(pk=message_id)
		#NpRequestAckEntry = NpMessages.objects.get(message_code ="NpRequestAck", submission_id = NpRequestEntry.submission_id, number = NpRequestEntry.number)
		#LogInput('got NpRequestAck id [message_id=%s]' % NpRequestAckEntry.message_id)
		
		LogInput('Found Message: %s[ServiceType=%s; MessageCode=%s; Number=%s; PortID=%s; DonorID=%s; RecipientID=%s; OriginationID=%s; DestinationID=%s], DB[MessageID=%s; Time=%s; Direction=%s; New=%s]' % (NpRequestEntry.message_code, NpRequestEntry.service_type, NpRequestEntry.message_code, NpRequestEntry.number, NpRequestEntry.port_id, NpRequestEntry.donor_id, NpRequestEntry.recipient_id, NpRequestEntry.origination_id, NpRequestEntry.destination_id, NpRequestEntry.message_id, NpRequestEntry.time_stamp, NpRequestEntry.direction, NpRequestEntry.new_message_unread))

		NpRequestCancel_dict=dict(
			ServiceType = str(NpRequestEntry.service_type) if NpRequestEntry.service_type is not None else str(''),
			MessageCode = str("NpRequestCancel"),
			Number = str(NpRequestEntry.number) if NpRequestEntry.number is not None else str(''),
			PortID = str(NpRequestEntry.port_id) if NpRequestEntry.port_id is not None else str(''),
			SubmissionID = str(NpRequestEntry.submission_id) if NpRequestEntry.submission_id is not None else str(''),
			DonorID = str(NpRequestEntry.donor_id) if NpRequestEntry.donor_id is not None else str(''),
			RecipientID = str(NpRequestEntry.recipient_id) if NpRequestEntry.recipient_id is not None else str(''),
			OriginationID = GetConfig("ORIGINATION_ID"),
			DestinationID = GetConfig("DESTINATION_ID"),
		)

		#deleting the empty elements from the NpRequest_dict
		for i in NpRequestCancel_dict.keys():
			if NpRequestCancel_dict[i]=='': NpRequestCancel_dict.pop(i)

		#LogInput('Message%s' % str(NpRequestCancel_dict))

		## Added by Hazim to set the fixed fields then store all the message to database
		instance = form.save(commit=False)
		instance.service_type = NpRequestCancel_dict.get('ServiceType')
		instance.message_code = NpRequestCancel_dict.get('MessageCode')
		instance.number = NpRequestCancel_dict.get('Number')
		instance.port_id = NpRequestCancel_dict.get('PortID')
		instance.submission_id = NpRequestCancel_dict.get('SubmissionID')
		instance.donor_id = NpRequestCancel_dict.get('DonorID')
		instance.recipient_id =  NpRequestCancel_dict.get('RecipientID')
		instance.origination_id =  NpRequestCancel_dict.get('OriginationID')
		instance.destination_id =  NpRequestCancel_dict.get('DestinationID')
		instance.direction = "OUT"
		instance.new_message_unread = "N"
		instance.save()
		
		# Send Message and get reply
		
		global cs_ret
		cs_ret = send_parse_save(NpRequestCancel_dict.get('MessageCode'),NpRequestCancel_dict)


		#LogInput('Message Sent ...')
		
		# update nprequest to read
		NpRequestEntry.new_message_unread = 'N'
		NpRequestEntry.save()
		
		LogInput('Updated Message: %s[ServiceType=%s; MessageCode=%s; Number=%s; PortID=%s; DonorID=%s; RecipientID=%s; OriginationID=%s; DestinationID=%s], DB[MessageID=%s; Time=%s; Direction=%s; New=%s]' % (NpRequestEntry.message_code, NpRequestEntry.service_type, NpRequestEntry.message_code, NpRequestEntry.number, NpRequestEntry.port_id, NpRequestEntry.donor_id, NpRequestEntry.recipient_id, NpRequestEntry.origination_id, NpRequestEntry.destination_id, NpRequestEntry.message_id, NpRequestEntry.time_stamp, NpRequestEntry.direction, NpRequestEntry.new_message_unread))

		
		queryset = NpMessages.objects.filter(direction="IN",message_code="NpRequest",new_message_unread="Y")
		
		if cs_ret['MessageCode'] == 'ErrorNotification':
			return render_to_response('web/IncomingRequests.html', {
				'reply_list': cs_ret,
				'back_color': "#F78181",
				'message_list': queryset,
				'page_name':PageName,
				'server':GetConfig("SOAP_CONNECTION"),
				})
		else:
			return render_to_response('web/IncomingRequests.html', {
				'reply_list': cs_ret,
				'back_color': "#A9F5A9",
				'message_list': queryset,
				'page_name':PageName,
				'server':GetConfig("SOAP_CONNECTION"),
				})


	return HttpResponseRedirect('/request/outgoing') # Redirect after POST

def SendNpRequestAccept(request):
	PageName = "Received Request"
	#LogInput('______________________________________________________')
	#LogInput('New Request Accept')
	if request.method == 'POST': # If the form has been submitted
		#LogInput('Form has been submitted')
		form = NpMessagesForm(request.POST) # A form bound to the POST data
		#LogInput('Checking submission')

		#Process the data in form.cleaned_data
		#those are values from form
		message_id = request.POST['message_id']
		#LogInput('Found Message id [message_id=%s]' % message_id)
		

		#get the request from data base
		NpRequestEntry = NpMessages.objects.get(pk=message_id)
		
		NpRequestAccept_dict=dict(
			ServiceType = str(NpRequestEntry.service_type) if NpRequestEntry.service_type is not None else str(''),
			MessageCode = str("NpRequestAccept"),
			Number = str(NpRequestEntry.number) if NpRequestEntry.number is not None else str(''),
			PortID = str(NpRequestEntry.port_id) if NpRequestEntry.port_id is not None else str(''),
			SubmissionID = str(NpRequestEntry.submission_id) if NpRequestEntry.submission_id is not None else str(''),
			DonorID = str(NpRequestEntry.donor_id) if NpRequestEntry.donor_id is not None else str(''),
			RecipientID = str(NpRequestEntry.recipient_id) if NpRequestEntry.recipient_id is not None else str(''),
			OriginationID = GetConfig("ORIGINATION_ID"),
			DestinationID = GetConfig("DESTINATION_ID"),
		)
		
		LogInput('Found Message: %s[ServiceType=%s; MessageCode=%s; Number=%s; PortID=%s; DonorID=%s; RecipientID=%s; OriginationID=%s; DestinationID=%s], DB[MessageID=%s; Time=%s; Direction=%s; New=%s]' % (NpRequestEntry.message_code, NpRequestEntry.service_type, NpRequestEntry.message_code, NpRequestEntry.number, NpRequestEntry.port_id, NpRequestEntry.donor_id, NpRequestEntry.recipient_id, NpRequestEntry.origination_id, NpRequestEntry.destination_id, NpRequestEntry.message_id, NpRequestEntry.time_stamp, NpRequestEntry.direction, NpRequestEntry.new_message_unread))


		#deleting the empty elements from the NpRequest_dict
		for i in NpRequestAccept_dict.keys():
			if NpRequestAccept_dict[i]=='': NpRequestAccept_dict.pop(i)

		#LogInput('Creating NpRequestAccept')

		## Added by Hazim to set the fixed fields then store all the message to database
		instance = form.save(commit=False)
		instance.service_type = NpRequestAccept_dict.get('ServiceType')
		instance.message_code = NpRequestAccept_dict.get('MessageCode')
		instance.number = NpRequestAccept_dict.get('Number')
		instance.port_id = NpRequestAccept_dict.get('PortID')
		instance.submission_id = NpRequestAccept_dict.get('SubmissionID')
		instance.donor_id = NpRequestAccept_dict.get('DonorID')
		instance.recipient_id =  NpRequestAccept_dict.get('RecipientID')
		instance.origination_id =  NpRequestAccept_dict.get('OriginationID')
		instance.destination_id =  NpRequestAccept_dict.get('DestinationID')
		instance.direction = "OUT"
		instance.new_message_unread = "N"
		instance.save()
		
		# Send Message and get reply
		global cs_ret
		cs_ret = send_parse_save(NpRequestAccept_dict.get('MessageCode'),NpRequestAccept_dict)

		#LogInput('Message Sent ...')
		
		# update nprequest to read
		NpRequestEntry.new_message_unread = 'N'
		NpRequestEntry.save()
		
		LogInput('Updated Message: %s[ServiceType=%s; MessageCode=%s; Number=%s; PortID=%s; DonorID=%s; RecipientID=%s; OriginationID=%s; DestinationID=%s], DB[MessageID=%s; Time=%s; Direction=%s; New=%s]' % (NpRequestEntry.message_code, NpRequestEntry.service_type, NpRequestEntry.message_code, NpRequestEntry.number, NpRequestEntry.port_id, NpRequestEntry.donor_id, NpRequestEntry.recipient_id, NpRequestEntry.origination_id, NpRequestEntry.destination_id, NpRequestEntry.message_id, NpRequestEntry.time_stamp, NpRequestEntry.direction, NpRequestEntry.new_message_unread))

		
		queryset = NpMessages.objects.filter(direction="IN",message_code="NpRequest",new_message_unread="Y")
		
		if cs_ret['MessageCode'] == 'ErrorNotification':
			return render_to_response('web/IncomingRequests.html', {
				'form': form,
				'reply_list': cs_ret,
				'back_color': "#F78181",
				'message_list': queryset,
				'page_name':PageName,
				'server':GetConfig("SOAP_CONNECTION"),
				})
		else:
			form2 = NpMessagesForm()
			return render_to_response('web/IncomingRequests.html', {
				'form': form2,
				'reply_list': cs_ret,
				'back_color': "#A9F5A9",
				'message_list': queryset,
				'page_name':PageName,
				'server':GetConfig("SOAP_CONNECTION"),
				})

	return HttpResponseRedirect('/request/incoming') # Redirect after POST


def SendNpRequest(request):
	PageName = "New Request"
	if request.method == 'POST': # If the form has been submitted
		#LogInput('Form has been submitted')
		instance=NpMessages()
		#form = NpMessagesForm(request.POST,instance=instance) # A form bound to the POST data
		form = NpMessagesForm(request.POST) # A form bound to the POST data
		#form=form_construct.save(commit=False)
		if form.is_valid(): # All validation rules pass
			#LogInput('Checking submission')

			#Process the data in form.cleaned_data
			number = form.cleaned_data['number']
			service_type = form.cleaned_data['service_type']
			donor_id = form.cleaned_data['donor_id']
			sim_card_number = form.cleaned_data['sim_card_number']
			company_flag = form.cleaned_data['company_flag']
			cpr = form.cleaned_data['cpr']
			passport_number = form.cleaned_data['passport_number']
			comments = form.cleaned_data['comments']

			NpRequest_dict=dict(
				ServiceType = str(service_type) if service_type is not None else str('') ,
				MessageCode = str("NpRequest"),
				Number = number if number is not None else str(''),
				DonorID = str(donor_id) if donor_id is not None else str(''),
				RecipientID = GetConfig("ORIGINATION_ID"),
				SimCardNumber = str(sim_card_number)  if sim_card_number is not None else str(''),
				CompanyFlag = str(company_flag)  if company_flag is not None else str(''),
				CPR = str(cpr) if cpr is not None else str(''),
				PassportNumber = str(passport_number)  if passport_number is not None else str(''),
				Comments = str(comments) if comments is not None else str(''),
				OriginationID = GetConfig("ORIGINATION_ID"),
				DestinationID = GetConfig("DESTINATION_ID"),
			)

			#deleting the empty elements from the NpRequest_dict
			for i in NpRequest_dict.keys():
				if NpRequest_dict[i]=='': NpRequest_dict.pop(i)
			
			
			#Saving the form parameters before saving the reply from the CS
			#there is an indintation problem, that's why it's like that
			#form.message_code='NpRequest'
			#form.save()

			## Check if company_flag is set then add the commercial_reg_number
			if company_flag == "Y":
				commercial_reg_number = form.cleaned_data['commercial_reg_number']
				NpRequest_dict['CommercialRegNumber']=str(commercial_reg_number) if commercial_reg_number is not None else str('')
				#LogInput('commercial registratin id has been assigned')
			
			## Auto generate the Submission ID
			if request.POST['submission_auto'] == "0":
				submission_id = form.cleaned_data['submission_id']
				NpRequest_dict['SubmissionID'] = str(submission_id) if submission_id is not None else str('')
			
			elif request.POST['submission_auto'] == "1" and number is not None:
				now = datetime.datetime.now()
				submission_id = GetConfig("ORIGINATION_ID") + "-" + str(now.year) + "-" + str(number)
				#instance.submission_id = submission_id
				NpRequest_dict['SubmissionID'] = str(submission_id) if submission_id is not None else str('')
			else:
				submission_id = ""
				#instance.submission_id = submission_id
				NpRequest_dict['SubmissionID'] = str(submission_id) if submission_id is not None else str('')

			##
			
			
			#LogInput('Creating NpRequest')
			#LogInput('New Message OUT: NpRequest%s' % str(NpRequest_dict))

			global cs_ret
			cs_ret = send_parse_save(NpRequest_dict['MessageCode'],NpRequest_dict)
			#LogInput('The return of send_parse_save function is %s '%str(cs_ret))


			#LogInput('Submission Complete reopening the new request page ...')

			#return HttpResponseRedirect('/request/request') # Redirect after POST
			
			## this will check if the reply is error then resend the same form, if not make new form
			if cs_ret['MessageCode'] == 'ErrorNotification':
				return render_to_response('web/SendNpRequest.html', {
					'form': form,
					'reply_list': cs_ret,
					'back_color': "#F78181",
					'page_name':PageName,
					'server':GetConfig("SOAP_CONNECTION"),
					}
				)
			else:
				form2 = NpMessagesForm()
				return render_to_response('web/SendNpRequest.html', {
					'form': form2,
					'reply_list': cs_ret,
					'back_color': "#A9F5A9",
					'page_name':PageName,
					'server':GetConfig("SOAP_CONNECTION"),
					}
				)
				
		else:
			#LogInput('Submission is not Valid')
			form = NpMessagesForm(request.POST, instance=instance)

	else:
		form = NpMessagesForm()
		#LogInput('New Form is created, ready to be filled and submitted')

	return render_to_response('web/SendNpRequest.html', {
		'form': form,
		'page_name':PageName,
		'server':GetConfig("SOAP_CONNECTION"),
		}
	)

