import base64
from base64 import b64encode
import datetime
import json
import os
# import urllib
import urllib.request as urllib
from urllib.request import urlopen
import urllib.parse



###################
# DEFINE VARIABLES
###################

#  	ASANA_WORKSPACE_ID
# 	ASANA_API_KEY

workspace_id = 'xxx'
thirty_days_ago = datetime.datetime.now() - datetime.timedelta(30)
yesterday = datetime.datetime.now() - datetime.timedelta(1)
modified_since_param = (datetime.datetime.now() - datetime.timedelta(90)).strftime('%Y-%m-%dT00:00:00Z')

apikey = 'xxx'
apikeyencoded = b64encode(bytes(apikey, "ascii")).decode("ascii")
#apikeyencoded = b64encode(b"0/97cc0274d52812ecc162f851c1f8283c").decode("ascii")
basic_auth = 'Basic ' + str(apikeyencoded)
#print (basic_auth)
#bearer_auth = 'Bearer ' + apikey
#print (bearer_auth)

overdue_comment_text = 'Automatische Erinnerung: Fälligkeitstermin der Aufgabe überschritten. Bitte um Kommentar. ~~~ Автоматическое напоминание: эта задача просрочена. Прошу прокомментировать. ~~~ Automatic reminder: this task is past its due date. Please comment on this.'

stale_comment_text = 'Automatische Erinnerung: diese Aufgabe wird alt. Bitte um Kommentar, wenn es noch Priorität hat. Oder schliessen Sie die Aufgabe! ~~~ Это дружественное напоминание о том, что эта задача становится устаревшей. Eсли она  по-прежнему приоритет, прошу прокомментировать. Или стереть задачу если она не нужна. ~~~ This is a friendly reminder that this task is getting stale. Please update it if its still a priority. Or kill it.'



###################
# TESTING Asana API access via python, not using the ASANA-PYTHONG client library
###################

# Simple test that urllib is imported correctly.
#html = urllib.request.urlopen('https://arstechnica.com').read()
#print(html)

# Simple test that urllib HEADERS are setup and authorization works.
request1 = urllib.request.Request('https://app.asana.com/api/1.0/users/me')
request1.add_header('Authorization', basic_auth)
result1 = urllib.request.urlopen(request1)
response1 = json.load(result1)
print (response1)



###################
# SCRIPT STARTS
###################

# python functions?
def data_for(path):
	request = urllib.request.Request('https://app.asana.com/api/1.0' + path)
	print('API requested from :::::: ' + 'https://app.asana.com/api/1.0' + path)
	
	request.add_header('Authorization', basic_auth)
	result = urllib.request.urlopen(request)
	return json.load(result)['data']
	
    #request = urllib.request.urlopen('https://app.asana.com/api/1.0' + path)
    #request.add_header('Authorization', basic_auth)
    #return json.load(urllib.urlopen(request))['data']

def comment_on_task(task_id, comment_text):
	data = urllib.parse.urlencode({'text': comment_text})
 
	request = urllib.request.Request('https://app.asana.com/api/1.0/tasks/' + str(task_id) + '/stories', data)
	print('API requested from :::::: ' + 'https://app.asana.com/api/1.0/tasks/' + str(task_id) + '/stories', data)
	
	request.add_header('Authorization', basic_auth)
	result = urllib.request.urlopen(request)
	return result
	
	#request = urllib.request.urlopen('https://app.asana.com/api/1.0/tasks/' + str(task_id) + '/stories', data)
    #request.add_header('Authorization', basic_auth)
    #return urllib.urlopen(request)

#get all USERS
users = data_for('/users')

#cycle through USERS
for user in users:
	if user['name'] == 'George':
		print ('FOUND GEORGE!')
