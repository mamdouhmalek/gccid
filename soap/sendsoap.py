from core_send import *
from handle_in_message import *

#NpRequest, NpExecute, NpRequestAccept, NpExecuteComplete are pre-set in the parent file
#and they are at the same time your  options
#you can directly assign them here at this file.

#We get the NpRequest from the form posted from the website

 
def send_parse_save(message, array):
	#Sending messages to CS	
	#result = SendSOAPMessage('SendNpRequest', NpRequest)
		
	#LogInput('Sending SendSOAPMessage ...')
	result = SendSOAPMessage(message, array)
	
	#parsing the returned xml from suds and returning dictionary
	#LogInput('SendSOAPMessage finished, now parsing ...%s'%str(result))
	Dict = myparser(result)
	
	#LogInput('Finished parsing ...%s',str(Dict))
	#LogInput('Now saving the outgoing/incoming messages ...')
	
	# Currently only outgoing NpRequest needs to be saved, the rest of the messages gets saved before here
	if message == 'NpRequest':
		#Saving the out going NpRequest Messages
		client_save_out(array, Dict)
	
	
	#Saving the returned parsed xml from suds
	#LogInput('Saving the incoming reply ...')
	client_save_in(Dict) 
	#LogInput('Finished Saving, DONE')
	
	return Dict
	
'''
Dict['ServiceType'], 
			Dict['MessageCode'], 
			Dict['Number, PortID'], 
			Dict['SubmissionID'], 
			Dict['DonorID'], 
			Dict['RecipientID'], 
			Dict['OriginationID'], 
			Dict['DestinationID']
'''			
