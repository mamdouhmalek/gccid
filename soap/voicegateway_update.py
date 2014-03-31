from configuration import GetConfig, LogInput, GetTimeStamp
from web.models import Number_Portability
import datetime
import os

def UpdateVoiceGateway(InMessage):
	LogInput('UpdateVoiceGateway  -  1')

	CustomerDataBase = 'vgw'

	## This is only for the report files naming and content
	#LogInput('Lightspeed Update: [Number=%s; SubscriptionNetworkID=%s]' % (PhoneNumber, NewRoute))
	now = datetime.datetime.now()
	year = "0" + str(now.year) if len(str(now.year)) == 1 else str(now.year)
	month = "0" + str(now.month) if len(str(now.month)) == 1 else str(now.month)
	day = "0" + str(now.day) if len(str(now.day)) == 1 else str(now.day)

	dir =  GetConfig("ROOT_DIR") + '/site/md/report/ported/' + year + "/" + month
	if not os.path.exists(dir):
		os.makedirs(dir)

	ReportFileName = dir + "/" + day + '-' + month + '-' + year + ".csv"
	# Check if the file exist, if not make the header of the table in the file
	if not os.path.isfile(ReportFileName):
		ReportFile = open(ReportFileName, "a")
		NewLogReport = "Time,Status,Number,New Route,Old Route\n"
		ReportFile.write("".join(NewLogReport))
	else:
		ReportFile = open(ReportFileName, "a")
	#####################

	LogInput('UpdateVoiceGateway  -  2')
	LogInput('Updating Database with New route')

	
	ServiceType = InMessage.ServiceType
	MessageCode = InMessage.MessageCode
	PortID = InMessage.PortID
	#OriginationID = InMessage.OriginationID
	#DestinationID = InMessage.DestinationID
	## Set the number before updating	#############
	PhoneNumber = str(InMessage.Number)

	LogInput('UpdateVoiceGateway  -  3')
	# added for the deactivation if Deactivation then get the different message 
	if InMessage.MessageCode == "NpDeactivateBroadcast":
		LogInput('UpdateVoiceGateway  -  4')

		LogInput('We are now at NpDeactivateBroadcast updating database:')
		PhoneNumber = InMessage.Number
		SubscriptionNetworkID = InMessage.SubscriptionNetworkID
		BlockID = InMessage.BlockID
		LogInput('Incoming information to VoiceGateway Database with %s, %s, SubscriptionNetworkID = %s, BlockID = %s' % (PhoneNumber, PortID, SubscriptionNetworkID, BlockID))	
		LogInput('UpdateVoiceGateway  -  5')

	else:	
		LogInput('UpdateVoiceGateway  -  6')

		DonorID = InMessage.DonorID
		RecipientID = InMessage.RecipientID
		NewRoute = InMessage.NewRoute
		PortingDatetime = InMessage.PortingDatetime
		LogInput('Incoming information to VoiceGateway Database with %s, %s, %s, %s, %s, %s' % (PhoneNumber, NewRoute, PortID, DonorID, RecipientID, PortingDatetime))		
		LogInput('UpdateVoiceGateway  -  7')

	LogInput('UpdateVoiceGateway  -  8')
	if InMessage.MessageCode == "NpDeactivateBroadcast":
		LogInput('UpdateVoiceGateway  -  9')
		PhoneNumber = InMessage.Number
		try:
			handler = Number_Portability.objects.using(CustomerDataBase).get(number=PhoneNumber)
			LogInput('UpdateVoiceGateway  -  10')
			
			if GetConfig("ENABLE_VOICEGATWAY_UPDATE") == "TRUE":
				LogInput('UpdateVoiceGateway  -  11')
				handler.delete(using=CustomerDataBase)
				LogInput('UpdateVoiceGateway  -  11.5')
			else:
				LogInput('UpdateVoiceGateway  -  12')
				LogInput('Voice Gateway Database update option is disabled')
	
			LogInput('UpdateVoiceGateway  -  13')
	
			# save to local DB
			if GetConfig("ENABLE_LOCALDB_UPDATE") == "TRUE":
				LogInput('UpdateVoiceGateway  -  14')
				try:
					handler.delete()
				except:
					LogInput('UpdateVoiceGateway  -  14.5')
					LogInput("Couldn't be deleted from local database")
			else:
				LogInput('UpdateVoiceGateway  -  15')
				LogInput('Local Database update option is disabled')
		except:
			LogInput('Number %s is not in voice gateway database, the number could be removed from before' % PhoneNumber)
	
		LogInput('UpdateVoiceGateway  -  16')

		LogInput('%s: Deactivated Route Number [Number=%s; SubscriptionNetworkID=%s]' % (GetConfig("COMPANY_NAME"), PhoneNumber, InMessage.BlockID))
		LogInput('UpdateVoiceGateway  -  17')
	
		NewLogReport = "%s,Deactivated,%s,%s,%s" % (GetTimeStamp()[:-4],PhoneNumber,InMessage.BlockID,InMessage.SubscriptionNetworkID)
		LogInput('UpdateVoiceGateway  -  18')

		ReportFile.write("".join(NewLogReport))
		ReportFile.write("".join("\n"))

		LogInput('UpdateVoiceGateway  -  19')

	#if Number_Portability.objects.using(CustomerDataBase).filter(destination=PhoneNumber).update(destination=PhoneNumber, origin=NewRoute):
		
	#if Number_Portability.objects.using(CustomerDataBase).filter(destination=PhoneNumber).update(destination=PhoneNumber, origin=NewRoute):
	elif Number_Portability.objects.using(CustomerDataBase).filter(number = PhoneNumber):
		# Update local DB
		#Number_Portability.objects.filter(destination=PhoneNumber).update(destination=PhoneNumber, origin=NewRoute)

		LogInput('Updating entry')


		# Update customer DB
		handler = Number_Portability.objects.using(CustomerDataBase).get(number = PhoneNumber)
		old_route = handler.rn
		
		LogInput('Old Handler : %s, %s, %s, %s, %s, %s]' % (handler.number, handler.portid, handler.rn, handler.recipient, handler.doner, handler.date_ported))

		#handler.number = PhoneNumber
		handler.portid = PortID
		handler.rn = NewRoute
		handler.recipient = RecipientID
		handler.doner = DonorID
		handler.date_ported = PortingDatetime

		LogInput('New Handler : %s, %s, %s, %s, %s, %s]' % (handler.number, handler.portid, handler.rn, handler.recipient, handler.doner, handler.date_ported))

		LogInput('ENABLE_VOICEGATWAY_UPDATE = %s' % GetConfig("ENABLE_VOICEGATWAY_UPDATE"))
		LogInput('%s: Before Updating Route To [Number=%s; SubscriptionNetworkID=%s]' % (GetConfig("COMPANY_NAME"), PhoneNumber, NewRoute))
		

		# save to Remote DB
		if GetConfig("ENABLE_VOICEGATWAY_UPDATE") == "TRUE":
			LogInput('Updating customer DB')
			handler.save(using=CustomerDataBase)
			LogInput('customer DB updated')
		else:
			LogInput('Voice Gateway Database update option is disabled')

		# save to local DB
		if GetConfig("ENABLE_LOCALDB_UPDATE") == "TRUE":
			LogInput('Updating local DB')
			handler.save()
			LogInput('local DB updated')
		else:
			LogInput('Local Database update option is disabled')
	
		LogInput('%s: Update Route To [Number=%s; SubscriptionNetworkID=%s]' % (GetConfig("COMPANY_NAME"), PhoneNumber, NewRoute))
		
		NewLogReport = "%s,update,%s,%s,%s" % (GetTimeStamp()[:-4],PhoneNumber,NewRoute,old_route)
	
		ReportFile.write("".join(NewLogReport))
		ReportFile.write("".join("\n"))

	else:
		LogInput('Creating new entry')

		handler = Number_Portability(
										number = PhoneNumber, 
										rn = NewRoute, 
										recipient = RecipientID,
										portid = PortID,
										doner = DonorID,
										date_ported = PortingDatetime,
									)
		# save to customer DB
		# save to Remote DB
		if GetConfig("ENABLE_VOICEGATWAY_UPDATE") == "TRUE":
			handler.save(using=CustomerDataBase)
			LogInput('new entry customer DB')
		else:
			LogInput('Voice Gateway Database update option is disabled')

		# save to local DB
		if GetConfig("ENABLE_LOCALDB_UPDATE") == "TRUE":
			handler.save()
			LogInput('new entry local DB')
		else:
			LogInput('Local Database update option is disabled')
	
		LogInput('%s: New Route [Number=%s; SubscriptionNetworkID=%s]' % (GetConfig("COMPANY_NAME"), PhoneNumber, NewRoute))

		NewLogReport = "%s,new,%s,%s," % (GetTimeStamp()[:-4],PhoneNumber,NewRoute)
	
		ReportFile.write("".join(NewLogReport))
		ReportFile.write("".join("\n"))

	ReportFile.close()
	
	return None