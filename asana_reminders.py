###################
# DEFINE LIBRARIES
###################

import base64
from base64 import b64encode
import datetime
import json
import os

# GD 2019-01-04: I am using URLLIB here but everyone is recommending switching to REQUESTS. Need to do that! 

import urllib.request as urllib
from urllib.request import urlopen
import urllib.parse



###################
# DEFINE VARIABLES
###################

#  	ASANA_WORKSPACE_ID
# 	ASANA_API_KEY

workspace_id = 'xxx'
thirty_days_ago = datetime.datetime.now() - datetime.timedelta(45)
yesterday = datetime.datetime.now() - datetime.timedelta(1)
modified_since_param = (datetime.datetime.now() - datetime.timedelta(90)).strftime('%Y-%m-%dT00:00:00Z')

apikey = 'xxx'
apikeyencoded = b64encode(bytes(apikey, "ascii")).decode("ascii")
#apikeyencoded = b64encode(b"0/97cc0274d52812ecc162f851c1f8283c").decode("ascii")
basic_auth = 'Basic ' + str(apikeyencoded)
#print (basic_auth)
#bearer_auth = 'Bearer ' + apikey
#print (bearer_auth)

overdue_comment_text = 'Bitte um ein Update zu dieser Aufgabe. Schreiben Sie ein Kommentar falls es etwas neues gibt oder wenn Hilfe vom Team notwendig ist. ~~~[RU] Напоминание: эта задача просрочена. Прошу прокомментировать. ~~~[ЕN] This task is past its due date. Please write a comment with an update.'

stale_comment_text = 'Aufgabe älter als 30 Tage. Bitte erledigen Sie die Aufgabe oder schreiben ein Kommentar warum die Aufgabe nicht erledigt werden kann. ~~~[RU] Напоминание: эта задача становится устаревшей - сделана более 30 дней назад. Прошу решить задачу или прокомментировать. ~~~[EN] This task is getting old - created over 30 days ago. Please complete it or add a comment.'



###################
# TESTING Asana API access via python, not using the ASANA-PYTHONG client library
###################

# Simple test that urllib is imported correctly.
#html = urllib.request.urlopen('https://arstechnica.com').read()
#print(html)

# Simple test that urllib HEADERS are setup and authorization works.
#request1 = urllib.request.Request('https://app.asana.com/api/1.0/users/me')
#request1.add_header('Authorization', basic_auth)
#result1 = urllib.request.urlopen(request1)
#response1 = json.load(result1)
#print (response1)



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

	request = urllib.request.Request('https://app.asana.com/api/1.0/tasks/' + str(task_id) + '/stories', data=bytes(data, "ascii"))
	request.add_header('Authorization', basic_auth)
	request.add_header('Content-Type', 'application/x-www-form-urlencoded')
	result = urllib.request.urlopen(request)
	# NOT SURE how to print full request URL payload string... learn!
	#print ('Full URL for the comment :::::: ' + str(result))
	return result
	
	#request = urllib.request.urlopen('https://app.asana.com/api/1.0/tasks/' + str(task_id) + '/stories', data)
    #request.add_header('Authorization', basic_auth)
    #return urllib.urlopen(request)

#get all USERS
users = data_for('/users')

#cycle through USERS
for user in users:
	if user['name'] == 'George':

		tasks = data_for('/tasks?workspace=' + workspace_id + '&assignee=' + str(user['id']) + '&modified_since=' + modified_since_param)
		i = 0
		
		#cycle through TASKS
		for task in tasks:
			print ('[{}/{} tasks for {}]'.format(i, len(tasks), user['name']))

			task_data = data_for('/tasks/' + str(task['id']))
			stories = data_for('/tasks/' + str(task['id']) + '/stories')

			if 'due_on' in task_data and task_data['due_on'] is not None and task_data['completed'] is not True:
				due_date = datetime.datetime.strptime(task_data['due_on'], '%Y-%m-%d')
				if due_date < yesterday:
					print (':::::: OVERDUE caught! ::::::')
					comment_on_task(task['id'], overdue_comment_text)
					print (':::::: OVERDUE; commented ::::::')
					### BREAK LOOP ###
					#raise SystemExit('EXIT: Just one success is enough for now...')

			if len(stories) > 0 and datetime.datetime.strptime(stories[-1]['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ') < thirty_days_ago and task_data['completed'] is not True:
				print (':::::: STALE caught! ::::::')
				comment_on_task(task['id'], stale_comment_text)
				print (':::::: STALE; commented ::::::')
				### BREAK LOOP ###
				#raise SystemExit('EXIT: Just one success is enough for now...')

			i += 1

print ('done!')
