from configuration import GetConfig, LogInput
from django.core.mail import send_mail
from django.core import mail


def send_email_now(InMessage):
	LogInput('In send_email_now  1')
	
	recipient_list = GetConfig("RECIPIENT_LIST")
	from_email = GetConfig("FROM_EMAIL")

	LogInput('In send_email_now  2')

	subject = ''
	message = ''

	LogInput('In send_email_now  3')

	if str(str(InMessage.message_code))=='NpRequest':
		subject = ('New Request for #: ' + str(InMessage.number))
		message = 'Hello,\n\nYou have received new request that require your attention before timeout.\n\nNew Request:\nFrom:\t' + str(InMessage.recipient_id) + '\n' + 'Phone #:\t' + str(InMessage.number) + '\n' + 'Port ID:\t' + str(InMessage.port_id) + '\n\nPlease accept or reject the request: ' + GetConfig("SERVER_URL") + '/request/incoming/\n\nThank you,\n4GTSS NPG System'

	LogInput('In send_email_now  4')
	
	if str(str(InMessage.message_code))=="NpRequestCancel":
		subject = ('Canceled Request for #: ' + str(InMessage.number))
		message = 'Hello,\n\nThe following request has been canceled.\n\nRequest Information:\nFrom:\t' + str(InMessage.recipient_id) + '\n' + 'Phone #:\t' + str(InMessage.number) + '\n' + 'Port ID:\t' + str(InMessage.port_id) + '\n\nThe request has been removed from: ' + GetConfig("SERVER_URL") + '/request/incoming/\n\nThank you,\n4GTSS NPG System'

	LogInput('In send_email_now  5')
	
	if str(str(InMessage.message_code))=="NpRequestReject":
		subject = ('Rejected Request for #: ' + str(InMessage.number))
		message = 'Hello,\n\nYour request has been rejected.\n\nRejected Reason:\n'+ str(InMessage.reject_code) + '\n' + str(InMessage.comments) +'\n\nRequest Information:\nFrom:\t' + str(InMessage.recipient_id) + '\n' + 'Phone #:\t' + str(InMessage.number) + '\n' + 'Port ID:\t' + str(InMessage.port_id) + '\n\nThe request has been removed from: ' + GetConfig("SERVER_URL") + '/request/incoming/\n\nThank you,\n4GTSS NPG System'

	LogInput('In send_email_now  6')
	
	if str(str(InMessage.message_code))=="NpRequestAccept":
		subject = ('Accepted Request for #: ' + str(InMessage.number))
		message = 'Hello,\n\nYour request has been executed .\n\nRequest Information:\nFrom:\t' + str(InMessage.recipient_id) + '\n' + 'Phone #:\t' + str(InMessage.number) + '\n' + 'Port ID:\t' + str(InMessage.port_id) + '\n\nThe request has been removed from: ' + GetConfig("SERVER_URL") + '/request/outgoing/\n\nThank you,\n4GTSS NPG System'

	LogInput('In send_email_now  7')
	
	if str(str(InMessage.message_code))=="ErrorNotification":
		subject = ('Error Notification for Order: ' + str(InMessage.port_id))
		message = 'Hello,\n\nThere is an error that require your attention .\n\nRequest Information:\n' + 'Error Code:\t' + str(InMessage.error_code) + '\n' + 'Comments:\t' + str(InMessage.comments) + '\n' + 'Port ID:\t\t' + str(InMessage.port_id) + '\n\nView Error: ' + GetConfig("SERVER_URL") + '/request/search/' + str(InMessage.message_id) + '\nView Request: ' + GetConfig("SERVER_URL") + '/request/search/' + str(InMessage.related_message_id) + '\nThe request has been removed from: ' + GetConfig("SERVER_URL") + '/request/outgoing/\n\nThank you,\n4GTSS NPG System'

	LogInput('In send_email_now  8')
	
	'''
	connection = mail.get_connection()
	
	# Manually open the connection
	connection.open()
	
	# Construct an email message that uses the connection
	email1 = mail.EmailMessage(subject, message, from_email,
	                          ['hazim.samour@solutionsfortelecom.com'], connection=connection)
	email1.send() # Send the email
	
	# Construct two more messages
	email2 = mail.EmailMessage(subject, message, from_email,
	                          ['bahaa.latif@solutionsfortelecom.com'], connection=connection)
	email3 = mail.EmailMessage(subject, message, from_email,
	                          ['hazim.samour@4gtss.com'], connection=connection)
	
	# Send the two emails in a single call -
	#connection.send_messages([email1, email2, email3])
	# The connection was already open so send_messages() doesn't close it.
	# We need to manually close the connection.
	connection.close()
	'''
	
	results = send_mail(subject, message, from_email, recipient_list)
	

	LogInput('In send_email_now  9')
	

	
	#msg = mail.EmailMessage(subject, message, from_email, recipient_list)
	#msg.content_subtype = "html"  # Main content is now text/html
	
	#results = msg.send()
	#results = send_mail(subject, message, from_email, recipient_list, fail_silently=False, auth_user='noreply@np.lsc.com.bh', auth_password='lightspeed')
	#results = send_mail(subject, message, from_email, recipient_list, fail_silently=False, auth_user='noreply@4gtss.com', auth_password='lightspeed')
	#results = send_mail(subject, message, from_email, recipient_list)
	
	return results