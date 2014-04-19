import datetime
import os

def GetConfig(request):
	##################################
	# IP Acceptance
	if request == "ENABLE_IP_SCREENING":
		#return 'True'
		return 'False'

	if request == "ALLOWED_IP":
		return '192.168.5.3'

	##################################
	# Django Settings
	if request == "COMPANY_NAME":
		return '4GTSS'

	if request == "SERVER_URL":
		return 'http://81.22.16.240'

	if request == "ROOT_DIR":
		return '/4gtss/mount'

	##################################
	# Django Settings
	if request == "DEBUG":
		#return 'True'
		return 'False'

	if request == "TIME_ZONE":
		return 'Asia/Bahrain'

	##################################
	# Default/Main Database Settings
	if request == "DEFAULT_DB_HOST":
		return 'localhost'

	if request == "DEFAULT_DB_NAME":
		return 'md_system'

	if request == "DEFAULT_DB_USER":
		return 'md'

	if request == "DEFAULT_DB_PASSWORD":
		return 'pNcKyYw3qUyP7MxR'

	##################################
	# Voice Gateway Database Settings
	if request == "ENABLE_VOICEGATWAY_UPDATE":
		return 'TRUE'
		#return 'FALSE'
	
	# Keep duplicate of voice gateway database locally 
	if request == "ENABLE_LOCALDB_UPDATE":
		#return 'TRUE'
		return 'FALSE'

	if request == "VGW_DB_NAME":
		return 'porta-billing'
		#return 'vgwlive'

	if request == "VGW_TABLE_NAME":
		return 'Number_Portability'

	if request == "VGW_DB_HOST":
		return 'master.lsc.com.bh'

	if request == "VGW_DB_USER":
		return 'npreadwrite'

	if request == "VGW_DB_PASSWORD":
		return 'ky98bEY5tmXa'

	##################################
	# Operator's Settings
	if request == "ORIGINATION_ID":
		return 'LSCO'

	if request == "DESTINATION_ID":
		return 'CSYS'

	##################################
	# Central System Settings - SUDS Connection
	if request == "SOAP_CONNECTION":
		#return 'TEST'
		return 'LIVE'

	# For Live server
	if request == "CSL":
		return {
					'url' : 'https://m2m.npcs.bh/services/NpcdbService?wsdl',
					'user' : 'soap_lsco', 
					'password' : 'pass_4gtss', 
				}

	# For the test server
	if request == "CST":
		return {
					'url' : 'https://m2m.test.npcs.bh/services/NpcdbService?wsdl',
					'user' : 'soap_lsco', 
					'password' : 'pass_4gtss', 
				}

	##################################
	# XSD Settings
	if request == "XSD_LOCATION":
		return GetConfig("ROOT_DIR") + '/site/npg/soap/xsd/nptypes.xsd'

		# for windows use: 'M:/site/hazimsite/wsdl/nptypes.xsd'
		# for Linux use:   GetConfig("ROOT_DIR") + '/site/npg/wsdl/nptypes.xsd'

	##################################
	# E-Mail Settings
	if request == "ENABLE_EMAIL":
		return 'TRUE'

	if request == "AUTHENTICATE_USER":
		return 'noreply@lightspeed.local'

	if request == "AUTHENTICATE_PASS":
		return 'lightspeed'

	if request == "FROM_EMAIL":
		return 'noreply@4gtss.com'

	if request == "RECIPIENT_LIST":
		return [
					'hazim.samour@solutionsfortelecom.com',
					'khaled.sobhy@4gtss.com',
				]

##################################
# Logging Function
def LogInput(NewLog):
	now = datetime.datetime.now()
	
	year = "0" + str(now.year) if len(str(now.year)) == 1 else str(now.year)
	month = "0" + str(now.month) if len(str(now.month)) == 1 else str(now.month)
	day = "0" + str(now.day) if len(str(now.day)) == 1 else str(now.day)
	
	#dir = GetConfig("ROOT_DIR") + '/site/npg/report/' + year + "/" + month
	dir =  '/mnp/log/' + year + "/" + month
	
	if not os.path.exists(dir):
		os.makedirs(dir)

	LogFileName = dir + "/" + day
	LogFile = open(LogFileName, "a")
	
	TimeStamp = "[%s]  " % (GetTimeStamp())
	
	LogFile.write("".join(TimeStamp))
	LogFile.write("".join(NewLog))
	LogFile.write("".join("\n"))
	
	LogFile.close()

def GetTimeStamp():
	now = datetime.datetime.now()

	year = "0" + str(now.year) if len(str(now.year)) == 1 else str(now.year)
	month = "0" + str(now.month) if len(str(now.month)) == 1 else str(now.month)
	day = "0" + str(now.day) if len(str(now.day)) == 1 else str(now.day)
	hour = "0" + str(now.hour) if len(str(now.hour)) == 1 else str(now.hour)
	minute = "0" + str(now.minute) if len(str(now.minute)) == 1 else str(now.minute)
	second = "0" + str(now.second) if len(str(now.second)) == 1 else str(now.second)
	millisecond = str(now.microsecond / 1000)
	millisecond = "0" + millisecond if len(millisecond) == 2 else millisecond
	millisecond = "00" + millisecond if len(millisecond) == 1 else millisecond
		
	return "%s-%s-%s %s:%s:%s,%s" % (year,month,day,hour,minute,second,millisecond)
