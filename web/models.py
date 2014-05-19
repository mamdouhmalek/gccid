from django.db import models
from django.forms import ModelForm, Textarea
from configuration import GetConfig

#For Regular Expression validation/Field validation
from django.core.validators import RegexValidator
import re
SID = re.compile('^[A-Z]{4}[\-][0-9]{4}[\-][0-9]{8}$')
NUM = re.compile('^[0-9]{8}$')
SIM = re.compile('^[0-9]{18,19}$')
CPR = re.compile('^[0-9]{9}$')
CRN = re.compile('^[0-9]{1,7}[\/][0-9]{1,2}$')
PASN = re.compile('^([0-9A-Za-z]{5}|[0-9A-Za-z]{12})$')
CMNT = re.compile('^[a-zA-Z0-9\-\_\+\.\s]{1,100}$')
##########End of patterns############################
#new branch

class NpMessages(models.Model):
	
	LIVE_OPERATOR_CHOICES = (
        (u'LSCO', u'Operator A'),
	)
	
	ALL_OPERATOR_CHOICES = (
        (u'ASTS', u'ASTS - Ascentech Technical Services'),
        (u'ATIB', u'ATIB - Atyaf Telecommunications and Infrastructure Bahrain W.L.L'),
        (u'BABC', u'BABC - Bahrain Broadband Co. W.L.L'),
        (u'BCNT', u'BCNT - Business Communications Networks'),
        (u'BTCF', u'BTCF - Bahrain Telecommunications Company (BATELCO) B.S.C'),
        (u'BTCM', u'BTCM - Bahrain Telecommunications Company (BATELCO) B.S.C'),
        (u'BTCX', u'BTCX - Bahrain Telecommunications Company (BATELCO) B.S.C - Virtual'),
        (u'BTCY', u'BTCY - Bahrain Telecommunications Company (BATELCO) B.S.C - Virtual'),
        (u'CONB', u'CONB - 2Connect WLL.'),
        (u'CONX', u'CONX - 2Connect WLL. - Test'),
        (u'ELTA', u'ELTA - Elephant Talk Bahrain W.L.L'),
        (u'ETBC', u'ETBC - Etisalcom Bahrain Company W.L.L'),
        (u'ETBX', u'ETBX - Etisalcom Bahrain Company W.L.L - Virtual'),
        (u'GOLD', u'GOLD - Golden Star Telecommunications W.L.L.'),
        (u'KLAM', u'KLAM - Kalam Telecom Bahrain B.S.C Closed'),
        (u'KULA', u'KULA - Kulacom Communication S.P.C'),
        (u'LIFE', u'LIFE - Life Communication B.S.C Closed'),
        (u'LSCX', u'LSCX - Lightspeed Communications W.L.L - Virtual'),
        (u'MNAF', u'MNAF - Menatelecom W.L.L'),
        (u'MNAM', u'MNAM - Menatelecom W.L.L.'),
        (u'MVGT', u'MVGT - Moving Gulf Telecom W.L.L.'),
        (u'NTRC', u'NTRC - Northstart Technology Company W.L.L.'),
        (u'NUET', u'NUET - Nuetel Communications S.P.C'),
        (u'NUEV', u'NUEV - Nuetel Communications S.P.C - Virtual'),
        (u'RAPD', u'RAPD - Rapid Telecommunications W.L.L'),
        (u'VICL', u'VICL - Viacloud W.L.L.'),
        (u'VIVA', u'VIVA - VIVA Bahrain B.S.C. Closed'),
        (u'VIVF', u'VIVF - Viva'),
        (u'VIVX', u'VIVX - VIVA Bahrain B.S.C. Closed - Virtual'),
        (u'ZANF', u'ZANF - Zain Bahrain B.S.C. Closed'),
        (u'ZANM', u'ZANM - Zain Bahrain B.S.C. Closed'),
        (u'ZANX', u'ZANX - Zain Bahrain B.S.C. Closed - Virtual'),
        (u'CSYS', u'Central System'),
	)
	
	MESSAGE_CODE_CHOICES = (
        (u'MessageAck', u'MessageAck'),
        (u'NpRequest', u'NpRequest'),
        (u'NpRequestAck', u'NpRequestAck'),
        (u'NpRequestAccept', u'NpRequestAccept'),
        (u'NpRequestReject', u'NpRequestReject'),
        (u'NpRequestCancel', u'NpRequestCancel'),
        (u'NpExecute', u'NpExecute'),
        (u'NpExecuteBroadcast', u'NpExecuteBroadcast'),
        (u'NpExecuteComplete', u'NpExecuteComplete'),
        (u'NpDeactivate', u'NpDeactivate'),
        (u'NpDeactivateAck', u'NpDeactivateAck'),
        (u'NpDeactivateBroadcast', u'NpDeactivateBroadcast'),
        (u'NpDeactivateComplete', u'NpDeactivateComplete'),
        (u'NpQuery', u'NpQuery'),
        (u'NpQueryComplete', u'NpQueryComplete'),
        (u'NpBillingResolution', u'NpBillingResolution'),
        (u'NpBillingResolutionEnd', u'NpBillingResolutionEnd'),
        (u'NpBillingResolutionReceived', u'NpBillingResolutionReceived'),
        (u'NpBillingResolutionAlert', u'NpBillingResolutionAlert'),
        (u'NpBillingResolutionAlertReceived', u'NpBillingResolutionAlertReceived'),
        (u'ErrorNotification', u'ErrorNotification'),
	)
	
	SERVICE_TYPE_CHOICES = (
        (u'M', u'Mobile'),
        (u'F', u'Fixed'),
        (u'S', u'Special Services'),
	)
	
	YES_NO_CHOICES = (
		(u'Y', u'Yes'),
		(u'N', u'No'),
	)
	COMPANY_FLAG = (
		(u'Y', u'Yes - Company'),
		(u'N', u'No - Privet Customer'),
	)
	
	
	NEW_ROUTE_CHOICES = (
		(u'b02', u'ATIB - Atyaf Telecommunications and Infrastructure Bahrain W.L.L'),
		(u'b03', u'BABC - Bahrain Broadband Co. W.L.L'),
		(u'b04', u'BTCF - Bahrain Telecommunications Company (BATELCO) B.S.C'),
		(u'a01', u'BTCM - Bahrain Telecommunications Company (BATELCO) B.S.C'),
		(u'b01', u'CONB - 2Connect WLL.'),
		(u'b05', u'ELTA - Elephant Talk Bahrain W.L.L'),
		(u'b06', u'ETBC - Etisalcom Bahrain Company W.L.L'),
		(u'b07', u'GOLD - Golden Star Telecommunications W.L.L.'),
		(u'b14', u'KLAM - Kalam Telecom Bahrain B.S.C Closed'),
		(u'b08', u'KULA - Kulacom Communication S.P.C'),
		(u'b15', u'LIFE - Life Communication B.S.C Closed'),
		(u'b09', u'LSCO - Lightspeed Communications W.L.L'),
		(u'b10', u'MNAF - Menatelecom W.L.L'),
		(u'a04', u'MNAM - Menatelecom W.L.L.'),
		(u'b11', u'NUET - Nuetel Communications S.P.C'),
		(u'b12', u'RAPD - Rapid Telecommunications W.L.L'),
		(u'a03', u'VIVA - VIVA Bahrain B.S.C. Closed'),
		(u'b16', u'ZANF - Zain Bahrain B.S.C. Closed'),
		(u'a02', u'ZANM - Zain Bahrain B.S.C. Closed'),
	)
	
	DIRECTION_CHOICES = (
		(u'OUT', u'Going out of the mediation device to the Central System'),
		(u'IN', u'Coming in from the Central System'),
	)
	
	
	message_id = models.AutoField(primary_key=True, blank=True)
	related_message_id = models.IntegerField(max_length=30, blank=True, null=True)
	time_stamp = models.DateTimeField(auto_now=True, auto_now_add=True, blank=True, null=True)
	# The message code corresponding to the Porting message:i.e. NpRequest
	message_code = models.CharField(max_length=40, choices=MESSAGE_CODE_CHOICES, blank=True, null=True, db_index=True) 
	#Unique ID assigned by the Central System to be used in messages referring to this Porting case
	port_id = models.CharField("Port ID", max_length=30, blank=True, null=True, db_index=True) 
	number =  models.IntegerField("Phone Number", max_length=12, blank=True, null=True, validators=[RegexValidator(regex=NUM, message="You think we don't validate your input!!!")])
	#Type of telephone service (Mobile, Fixed or other Services)
	service_type = models.CharField(max_length=5, choices=SERVICE_TYPE_CHOICES, blank=True, null=True) 
	#The ID used by the Central System to identify the Donor Operator
	donor_id = models.CharField("Donor ID", max_length=8, choices=ALL_OPERATOR_CHOICES, blank=True, null=True)
	#The ID used by the Central System to identify the Recipient Operator
	recipient_id = models.CharField(max_length=8, choices=ALL_OPERATOR_CHOICES, blank=True, null=True)
	#The ID used by the Central System to identify the Originator
	origination_id = models.CharField(max_length=8, choices=ALL_OPERATOR_CHOICES, blank=True, null=True)
	#The ID used by the Central System to identify the Destination
	destination_id = models.CharField(max_length=8, choices=ALL_OPERATOR_CHOICES, blank=True, null=True)
	#The ID used by the Central System to identify the Destination
	subscription_network_id = models.CharField(max_length=8, choices=ALL_OPERATOR_CHOICES, blank=True, null=True) 
	block_id = models.CharField(max_length=8, choices=ALL_OPERATOR_CHOICES, blank=True, null=True)
	submission_id = models.CharField("Submission ID", max_length=28, blank=True, null=True, validators=[RegexValidator(regex=SID, message="You think we don't validate your input!!!")])
	#The integrated Circuit Card ID as written on the SIM card
	sim_card_number = models.CharField("SIM Card #", max_length=89, blank=True, null=True, validators=[RegexValidator(regex=SIM, message="You think we don't validate your input!!!")])
	#Used to indicate whether the Subscriber is an individual person (N) or a company (Y)
	company_flag = models.CharField("Company Flag", max_length=5, choices=COMPANY_FLAG, blank=True, null=True) 
	#Commercial Registration Number in case of a company
	commercial_reg_number = models.CharField("Commercial Registration", max_length=20, blank=True, null=True, validators=[RegexValidator(regex=CRN, message="You think we don't validate your input!!!")])
	passport_number = models.CharField("Passport Number", max_length=18, blank=True, null=True, validators=[RegexValidator(regex=PASN, message="You think we don't validate your input!!!")])
	#Central Population Registry number
	cpr = models.IntegerField("CPR #", max_length=19, blank=True, null=True, validators=[RegexValidator(regex=CPR, message="You think we don't validate your input!!!")])
	#Central Population Registry number
	reject_code = models.CharField(max_length=12, blank=True, null=True)
	new_route = models.CharField(max_length=9, choices=NEW_ROUTE_CHOICES, blank=True, null=True)
	# Bahaa please set date and time in here, final view should be as follows PortingDatetime=2011-10-30 08:00:00.000]
	porting_date_time = models.CharField(max_length=40, blank=True, null=True)
	# Aiman please verify
	error_code = models.CharField(max_length=30, blank=True, null=True)
	rejected_message_code = models.CharField(max_length=100, blank=True, null=True)
	comments = models.TextField(max_length=100, blank=True, null=True, validators=[RegexValidator(regex=CMNT, message="You think we don't validate your input!!!")])
	#Out from the Mediation Device or In to the Mediation Device
	direction = models.CharField(max_length=8, choices=DIRECTION_CHOICES, blank=True, null=True, db_index=True)
	# If message is new it will be set to Y, if it has been handled will be set to N
	new_message_unread = models.CharField(max_length=5, choices=YES_NO_CHOICES, blank=True, null=True, db_index=True)

	class Meta:
		db_table = "np_messages"

	
#	def __unicode__(self):
#		return self.NpMessages

class NpMessagesForm(ModelForm):
	"""
	Auto generated form to create Server models.
	"""
	class Meta:
		model = NpMessages
		fields = ('message_id', 'message_code', 'submission_id','number','service_type','sim_card_number','company_flag','cpr','commercial_reg_number', 'passport_number','comments','donor_id','reject_code','port_id','direction')
		widgets = {'comments': Textarea(attrs={'cols': 50, 'rows': 2}),
					}

## lightspeed voice gateway database table's structure

class Number_Portability(models.Model):
	i_number = models.AutoField(primary_key=True, blank=True) 
	destination =  models.CharField("Destination", max_length=32, blank=True, null=True)
	origin =  models.CharField("Route", max_length=32, blank=True, null=True)

	class Meta:
		db_table = GetConfig("VGW_TABLE_NAME")
	

## Rawabi voice gateway database table's structure
'''
class Number_Portability(models.Model):
	portid = models.CharField(max_length=100, blank=True) 
	b =  models.CharField(max_length=100, blank=True, null=True)
	number =  models.CharField(primary_key=True, max_length=100)
	recipient =  models.CharField(max_length=100, blank=True, null=True)
	doner =  models.CharField(max_length=100, blank=True, null=True)
	rn =  models.CharField(max_length=100, blank=True, null=True)
	date_ported =  models.CharField(max_length=100, blank=True, null=True)
	date_updated =  models.DateTimeField(auto_now=True, auto_now_add=True, blank=True, null=True)

	class Meta:
		db_table = GetConfig("VGW_TABLE_NAME")
'''
