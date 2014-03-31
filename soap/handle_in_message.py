## Logging added by Hazim
from configuration import GetConfig, LogInput
import time
from web.models import NpMessages as NpMessagesForm
import datetime

def client_save_out(message, reply):
	SetOutMessage = NpMessagesForm()

	SetOutMessage.time_stamp = datetime.datetime.now()
	SetOutMessage.service_type = message.get('ServiceType')
	SetOutMessage.message_code = message.get('MessageCode')
	SetOutMessage.number = message.get('Number')	
	SetOutMessage.origination_id = message.get('OriginationID')	
	SetOutMessage.destination_id = message.get('DestinationID')
	SetOutMessage.submission_id = message.get('SubmissionID')
	SetOutMessage.donor_id = message.get('DonorID')
	SetOutMessage.recipient_id = message.get('RecipientID')
	SetOutMessage.sim_card_number = message.get('SimCardNumber')
	SetOutMessage.company_flag = message.get('CompanyFlag')
	SetOutMessage.cpr = message.get('CPR')
	SetOutMessage.commercial_reg_number = message.get('CommercialRegNumber')
	SetOutMessage.passport_number = message.get('PassportNumber')
	SetOutMessage.comments = message.get('Comments')
	SetOutMessage.direction = 'OUT'

	MessageLog = 'New Message %s: %s[MessageCode=%s; ServiceType=%s; ' % (SetOutMessage.direction, SetOutMessage.message_code, SetOutMessage.message_code, SetOutMessage.service_type)

	if message.get('MessageCode') == 'NpRequest' and reply.get('MessageCode') == 'NpRequestAck':
		SetOutMessage.new_message_unread = "Y"
		SetOutMessage.port_id = reply.get('PortID')
		MessageLog +='PortID=%s; ' % SetOutMessage.port_id
		
	if message.get('MessageCode') == 'NpRequest' and reply.get('MessageCode') == 'ErrorNotification':
		SetOutMessage.new_message_unread = "N"
	
	SetOutMessage.save()
	
	LogInput('%s Number=%s; SubmissionID=%s; DonorID=%s; RecipientID=%s; OriginationID=%s; DestinationID=%s], DB[MessageID=%s; Time=%s; Direction=%s; New=%s]' % (MessageLog, SetOutMessage.number, SetOutMessage.submission_id, SetOutMessage.donor_id, SetOutMessage.recipient_id, SetOutMessage.origination_id,SetOutMessage.destination_id, SetOutMessage.message_id, SetOutMessage.time_stamp, SetOutMessage.direction, SetOutMessage.new_message_unread))

def client_save_in(InMessage):
	SetInMessage = NpMessagesForm()
	
	SetInMessage.time_stamp = datetime.datetime.now()
	SetInMessage.service_type = InMessage.get('ServiceType')
	SetInMessage.message_code = InMessage.get('MessageCode')
	SetInMessage.origination_id = InMessage.get('OriginationID')	
	SetInMessage.destination_id = InMessage.get('DestinationID')
	SetInMessage.port_id = InMessage.get('PortID')
	SetInMessage.direction = 'IN'							
	SetInMessage.new_message_unread = "N"

	MessageLog = 'New Message IN: %s[MessageCode=%s; ServiceType=%s; PortID=%s; ' % (SetInMessage.message_code, SetInMessage.message_code, SetInMessage.service_type, SetInMessage.port_id)

	if InMessage.get('MessageCode') != 'ErrorNotification':
		if InMessage.get('MessageCode') != u'MessageAck':
			SetInMessage.number = InMessage.get('Number')
			MessageLog += 'Number=%s; ' % (SetInMessage.number)
		
		if InMessage.get('MessageCode') == u'NpRequestAck':
			SetInMessage.submission_id = InMessage.get('SubmissionID')
			SetInMessage.donor_id = InMessage.get('DonorID')
			SetInMessage.recipient_id = InMessage.get('RecipientID')
			MessageLog += 'SubmissionID=%s; DonorID=%s; RecipientID=%s; ' % (SetInMessage.submission_id, SetInMessage.donor_id, SetInMessage.recipient_id)

		if InMessage.get('MessageCode') == u'NpDeactivateAck':
			SetInMessage.subscription_network_id = InMessage.get('SubscriptionNetworkID')	
			SetInMessage.block_id = InMessage.get('BlockID')
			MessageLog += 'SubscriptionNetworkID=%s; BlockID=%s; ' % (SetInMessage.subscription_network_id, SetInMessage.block_id)

	else:
		SetInMessage.comments = InMessage.get('Comments')
		SetInMessage.rejected_message_code = InMessage.get('RejectedMessageCode')
		SetInMessage.error_code = InMessage.get('ErrorCode')
		MessageLog += 'RejectedMessageCode=%s; ErrorCode=%s; Comments=%s; ' % (SetInMessage.rejected_message_code, SetInMessage.error_code, SetInMessage.comments)

	MessageLog += 'OriginationID=%s; DestinationID=%s]' % (SetInMessage.origination_id,SetInMessage.destination_id)

	SetInMessage.save()
	
	LogInput('%s, DB[MessageID=%s; Time=%s; Direction=%s; New=%s]' % (MessageLog, SetInMessage.message_id, SetInMessage.time_stamp, SetInMessage.direction, SetInMessage.new_message_unread))

	


# Database work - importing NpMessages model from the form app
# from save_send_reply import HandleIncomingMessage, SetMessageAck, SetNpRequestAck, SetNpDeactivateAck
# NpMessagesForm is used to store in the database and create a form at the same time.

# Storing the outgoing MessageAck message to database function
def HandleIncomingMessage(InMessage):
	#LogInput('Starting the process of storing the incoming message  %s' % InMessage.MessageCode)
	
	MessageLog = 'New Message IN: %s[' % InMessage.MessageCode
	#Message: MessageAck[ServiceType=M; MessageCode=MessageAck; PortID=VIVX-VIVA-20111216-00004; OriginationID=LSCO; DestinationID=CSYS]
	
	# getting the form modul and fill it up
	SetInMessage = NpMessagesForm()
	
	# Set the information for all the messages
	SetInMessage.time_stamp = datetime.datetime.now()
	SetInMessage.message_code = InMessage.MessageCode		# 
	SetInMessage.origination_id = InMessage.OriginationID	# This mandatory and it is sent with NpRequest by CS
	SetInMessage.destination_id = InMessage.DestinationID	# This mandatory and it is sent with NpRequest by CS
	SetInMessage.direction = 'IN'							# Generated by us to know if this incoming or outgoing
	
	#LogInput('Setting time stamp  %s' % SetInMessage.time_stamp)
	MessageLog += 'MessageCode=%s; ' % (InMessage.MessageCode)
	#LogInput('Handled Direction  %s' % SetInMessage.direction)
	

	# Set ServiceType, Number, DonorID, RecipientID for all messages but ErrorNotification, NpDeactivateComplete, NpBillingResolutionReceived, NpBillingResolutionEnd
	if SetInMessage.message_code in ("NpRequest", "NpRequestAck", "NpRequestAccept", "NpRequestReject", "NpRequestCancel", "NpExecuteComplete", "NpExecute", "NpDeactivate", "NpBillingResolution", "NpBillingResolutionAlert", "NpBillingResolutionAlertReceived", "NpExecuteBroadcast"):
		SetInMessage.service_type = InMessage.ServiceType
		SetInMessage.number = InMessage.Number
		SetInMessage.donor_id = InMessage.DonorID
		SetInMessage.recipient_id = InMessage.RecipientID
		
		MessageLog += 'ServiceType=%s; Number=%s; DonorID=%s; RecipientID=%s; ' % (InMessage.ServiceType,InMessage.Number,InMessage.DonorID, InMessage.RecipientID)
	
	if SetInMessage.message_code == "MessageAck":
		SetInMessage.service_type = InMessage.ServiceType
		MessageLog += 'ServiceType=%s; ' % ServiceType
	
	# Set PortID for all messages but NpRequest
	if SetInMessage.message_code in ("MessageAck", "NpRequestAck", "NpDeactivateAck", "ErrorNotification", "NpRequestAccept", "NpRequestReject", "NpRequestCancel", "NpExecuteComplete", "NpDeactivateBroadcast", "NpDeactivateComplete", "NpExecute", "NpDeactivate", "NpBillingResolution", "NpBillingResolutionReceived", "NpBillingResolutionEnd", "NpBillingResolutionAlert", "NpBillingResolutionAlertReceived","NpExecuteBroadcast"):
		
		SetInMessage.port_id = InMessage.PortID
		MessageLog += 'PortID=%s; ' % InMessage.PortID
			
	# Set the submission ID for NpRequest, NpRequestAccept, NpRequestReject, NpRequestCancel, NpRequestAck
	if SetInMessage.message_code in ("NpRequest", "NpRequestAck", "NpRequestAccept", "NpRequestReject", "NpRequestCancel"):
		SetInMessage.submission_id = InMessage.SubmissionID
		MessageLog += 'SubmissionID=%s; ' % InMessage.SubmissionID
	
	# Set SubscriptionNetworkID for NpDeactivateComplete, NpDeactivate, NpBillingResolution, NpBillingResolutionReceived, NpBillingResolutionEnd, NpBillingResolutionAlert, NpBillingResolutionAlertReceived, NpDeactivateAck
	if SetInMessage.message_code in ("NpDeactivateComplete", "NpDeactivateBroadcast", "NpDeactivate", "NpDeactivateAck", "NpBillingResolution", "NpBillingResolutionReceived", "NpBillingResolutionEnd", "NpBillingResolutionAlert", "NpBillingResolutionAlertReceived"):
		SetInMessage.new_route = InMessage.SubscriptionNetworkID
		MessageLog += 'SubscriptionNetworkID=%s; ' % InMessage.SubscriptionNetworkID
		
	# Set the Submission ID for NpRequest, NpRequestReject, ErrorNotification
	if SetInMessage.message_code in ("NpRequest", "NpRequestReject", "ErrorNotification"):
		SetInMessage.comments = InMessage.Comments
		SetInMessage.new_message_unread = "Y"	# set NpRequest, NpRequestReject", ErrorNotification to new message
		MessageLog += 'Comments=%s; ' % InMessage.Comments
	
	# Set the ErrorNotification
	if SetInMessage.message_code == "ErrorNotification":
		SetInMessage.rejected_message_code = InMessage.RejectedMessageCode
		SetInMessage.error_code = InMessage.ErrorCode
		MessageLog += 'RejectedMessageCode=%s; ErrorCode=%s; ' % (InMessage.RejectedMessageCode,InMessage.ErrorCode)
	
	# Set NpRequest
	if SetInMessage.message_code == "NpRequest":
		SetInMessage.port_id = InMessage.PortID
		SetInMessage.sim_card_number = InMessage.SimCardNumber
		SetInMessage.company_flag = InMessage.CompanyFlag
		SetInMessage.cpr = InMessage.CPR
		SetInMessage.commercial_reg_number = InMessage.CommercialRegNumber
		SetInMessage.passport_number = InMessage.PassportNumber
		
		MessageLog += 'PortID=%s; SimCardNumber=%s; CompanyFlag=%s; CPR=%s; CommercialRegNumber=%s; PassportNumber=%s; ' % (InMessage.PortID,InMessage.SimCardNumber,InMessage.CompanyFlag,InMessage.CPR,InMessage.CommercialRegNumber,InMessage.PassportNumber)
		
	if SetInMessage.message_code == "NpExecuteBroadcast":
		SetInMessage.new_route = InMessage.NewRoute
		SetInMessage.porting_date_time = InMessage.PortingDatetime
		
		MessageLog += 'NewRoute=%s; PortingDatetime=%s; ' % (InMessage.NewRoute,InMessage.PortingDatetime)
		
	if SetInMessage.message_code == "NpRequestAccept":
		pass
	
	if SetInMessage.message_code == "NpRequestReject":
		SetInMessage.reject_code = InMessage.RejectCode
	
	if SetInMessage.message_code == "NpRequestCancel":
		pass
	
	if SetInMessage.message_code == "NpExecuteComplete":
		pass
	
	if SetInMessage.message_code in ("NpDeactivateBroadcast", "NpDeactivateComplete", "NpDeactivateAck"):
		SetInMessage.service_type = InMessage.ServiceType
		SetInMessage.number = InMessage.Number
		SetInMessage.block_id = InMessage.BlockID # add it to data base
		
		MessageLog += 'ServiceType=%s; Number=%s; BlockID=%s; ' % (InMessage.ServiceType,InMessage.Number,InMessage.BlockID)
	
	if SetInMessage.message_code == "NpExecute":
		pass
	
	if SetInMessage.message_code == "NpDeactivate":
		#SetInMessage. = InMessage.BlockID # add it to data base
		pass
	
	if SetInMessage.message_code == "NpDeactivateBroadcast":
		pass
	

	if SetInMessage.message_code == "NpBillingResolution":
		pass
	
	if SetInMessage.message_code == "NpBillingResolutionReceived":
		SetInMessage.service_type = InMessage.ServiceType
		SetInMessage.number = InMessage.Number
		SetInMessage.donor_id = InMessage.DonorID

	if SetInMessage.message_code == "NpBillingResolutionEnd":
		SetInMessage.service_type = InMessage.ServiceType
		SetInMessage.number = InMessage.Number
		SetInMessage.donor_id = InMessage.DonorID
	
	if SetInMessage.message_code == "NpBillingResolutionAlert":
		SetInMessage.resolution_level = InMessage.ResolutionLevel
		MessageLog += 'ResolutionLevel=%s; ' % ResolutionLevel
	
	if SetInMessage.message_code == "NpBillingResolutionAlertReceived":
		pass
	
	MessageLog += 'OriginationID=%s; DestinationID=%s]' % (InMessage.OriginationID,InMessage.DestinationID)
	
	## This will send to the data base
	SetInMessage.save()
	
	LogInput('%s, DB[MessageID=%s; Time=%s; Direction=%s; New=%s]' % (MessageLog, SetInMessage.message_id, SetInMessage.time_stamp, SetInMessage.direction, SetInMessage.new_message_unread))
	#LogInput('SAVING TO DATA BASE  %s' % InMessage.MessageCode)

	## Send E-Mail only on receiving the messages inside the if statement 
	from soap.sendemail import send_email_now
	# The first if stetment was added for the ErrorNotification

	LogInput('In HandleIncomingMessage 40')

	if SetInMessage.message_code in ("ErrorNotification"):
		LogInput('In HandleIncomingMessage 41')
	
		if SetInMessage.rejected_message_code == "NpRequest":
			LogInput('In HandleIncomingMessage 42')
			try:
				LogInput('In HandleIncomingMessage 43')
				
				NpRequestEntry = NpMessagesForm.objects.get(message_code = "NpRequest", port_id = InMessage.PortID, new_message_unread = "Y")
				
				LogInput('In HandleIncomingMessage 44')
					
				LogInput('Found Message: %s[ServiceType=%s; MessageCode=%s; Number=%s; PortID=%s; DonorID=%s; RecipientID=%s; OriginationID=%s; DestinationID=%s], DB[MessageID=%s; Time=%s; Direction=%s; New=%s]' % (NpRequestEntry.message_code, NpRequestEntry.service_type, NpRequestEntry.message_code, NpRequestEntry.number, NpRequestEntry.port_id, NpRequestEntry.donor_id, NpRequestEntry.recipient_id, NpRequestEntry.origination_id, NpRequestEntry.destination_id, NpRequestEntry.message_id, NpRequestEntry.time_stamp, NpRequestEntry.direction, NpRequestEntry.new_message_unread))
		
				## Updateing the NpRequest with unread
				#old_new_message_unread = NpRequestEntry.new_message_unread
				NpRequestEntry.new_message_unread = "N"
				NpRequestEntry.save()

				LogInput('In HandleIncomingMessage 45')

				#LogInput('Updating %s # %s [new_message_unread = %s TO new_message_unread = %s]' % (NpRequestEntry.message_code,NpRequestEntry.message_id,old_new_message_unread,NpRequestEntry.new_message_unread))
				## This will send to the data base
				LogInput('Updated Message: %s[ServiceType=%s; MessageCode=%s; Number=%s; PortID=%s; DonorID=%s; RecipientID=%s; OriginationID=%s; DestinationID=%s], DB[MessageID=%s; Time=%s; Direction=%s; New=%s]' % (NpRequestEntry.message_code, NpRequestEntry.service_type, NpRequestEntry.message_code, NpRequestEntry.number, NpRequestEntry.port_id, NpRequestEntry.donor_id, NpRequestEntry.recipient_id, NpRequestEntry.origination_id, NpRequestEntry.destination_id, NpRequestEntry.message_id, NpRequestEntry.time_stamp, NpRequestEntry.direction, NpRequestEntry.new_message_unread))
				
				# the next line will send the message ID of the NpRequest to show it in the email that will be sent for the error notification
				SetInMessage.related_message_id = NpRequestEntry.message_id
				try:
					from soap.sendemail import send_email_now
					send_email_now(SetInMessage)
					LogInput('Email sent successfully for message: [MessageID=%s; MessageCode=%s; Number=%s]' % (NpRequestEntry.message_id, NpRequestEntry.message_code, NpRequestEntry.number))
				except:
					LogInput('Email was not sent successfully for message: [MessageID=%s; MessageCode=%s; Number=%s]' % (NpRequestEntry.message_id, NpRequestEntry.message_code, NpRequestEntry.number))			
				
			except:
				LogInput("Message NpRequest was not found in Database or it was set to read; Message[MessageCode=NpRequest; PortID=%s]" % (InMessage.PortID))
	
	elif SetInMessage.message_code in ("NpRequest", "NpRequestReject", "NpRequestCancel", "NpRequestAccept"):
		try:
			send_email_now(SetInMessage)
			LogInput('Email sent successfully for message: [MessageID=%s; MessageCode=%s; Number=%s]' % (SetInMessage.message_id, SetInMessage.message_code, SetInMessage.number))
		except:
			LogInput('Email was not sent successfully for message: [MessageID=%s; MessageCode=%s; Number=%s]' % (SetInMessage.message_id, SetInMessage.message_code, SetInMessage.number))