from json import dumps
from flask import Flask, request, jsonify
from validemail import check
from error import AccessError
from datetime import datetime, timedelta

app = Flask(__name__)

# GLOBAL VARIABLE BELOW
messages = [{
	'message_id':'', 
	'u_id':'', 
	'message':'', 
	'time_created':'', 
	'reacts':'', 
	'is_pinned':'',  
}]

channel = [{
    'name':'',
    'channel_id':'',
    'is_public': False, 
    'owner':[], # owner of the channel or slackr
    'member':[{ 
    	'u_id':'', 
    	'name_first':'', 
    	'name_last':'' 
    }], 
    'message' : [{
        'message' :'',
        'message_id':'',
        'user':'',
        'time_sent':'',
        'react_id':[],
        'pin': False
    }]
}]

user = [{
	'email': '',
	'password':'',
	'u_id':'',
	'token':'',
	'login': False, 
	'permission_id':'', #slackr
	'channel_list':[{
		'channel_id':'',
		'permission':'' # channel
		}]
	}]

login_user = {  # current user
	'first name':'',
	'last name':'',
	'handle':'',
	'email': '',
	'password':'',
	'u_id':'',
	'token':'',
	'permission_id':'',
	'channel_list':[{
		'channel_id':'',
		'permission':'' # channel
		}]
	}

# GLOBAL VARIABLE ABOVE


@app.route("/user/profile/setname", methods=['PUT'])
def user_profile_setname():
	name_first = request.form.get('name_first')
	name_last = request.form.get('name_last')
	token = request.form.get('token')	
	global user, login_user
	# ValueError when:
	# name_first is more than 50 characters
	if len(name_first) > 50:
		raise ValueError('First name must be less than 50 characters')
	# name_last is more than 50 characters
	elif len(name_last) > 50:
		raise ValueError('Last name must be less than 50 characters')
	# Update the authorised user's first and last name
	# Check if authorised by token
	for u in user:
		if token == u['token']:
			login_user['authorised'] = True
	# No Access if not authorised
	if login_user['authorised'] == False:
			AccessError("Access Denied: Non-authorised User")
	# Update name
	login_user['first name'] = name_first
	login_user['last name'] = name_last
	return dumps({})


@app.route("/user/profile/setemail", methods=['PUT'])
def user_profile_setemail():
	global user, login_user
	token = request.form.get('token')
	email = request.form.get('email')
	# Email entered is not a valid email
	if not check(email)=='Valid Email':
		raise ValueError('Invalid Email')
	# Email address is already being used by another user
	elif email in user['email']:
		raise ValueError('Email already registered')
	# Check if authorised by token
	for u in user:
		if token == u['token']:
			login_user['authorised'] = True
	# No Access if not authorised
	if login_user['authorised'] == False:
			AccessError("Access Denied: Non-authorised User")
	# Update the authorised user's email address
	login_user['email'] = email

	return dumps({})

@app.route("/user/profile/sethandle", methods=['PUT'])
def user_profile_sethandle():
	global user, login_user
	token = request.form.get('token')
	handle_str = request.form.get('handle_str')  
	# Value Error when:
	# handle_str is is between 3 and 20 characters
	if len(handle_str) > 20:
		if len(handle_str) < 3
			raise ValueError('Handle must be between 3 and 20 characters')
	# Check if authorised by token
	for u in user:
		if token == u['token']:
			login_user['authorised'] = True
	# No Access if not authorised
	if login_user['authorised'] == False:
			AccessError("Access Denied: Non-authorised User")
	# Update the authorised user's handle 
	# Assume that handle is in right format
	login_user['handle'] = handle_str
	return dumps({}) 

@app.route("/user/profile/uploadphoto", methods=['POST'])
def user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end, y_end):
	# this is not requried to be completed until iteration 3
	return dumps({})

@app.route("/standup/start", methods=['POST'])
def standup_start():
	global channel, user, login_user
	token = request.form.get('token')
	channel_id = request.form.get('channel_id')
	# Value Error when:
	# Channel (based on ID) does not exist
	validChannel = False
	for c in channel:
		if channel_id == c['channel_id']:
			validChannel = True
			currentChannel = c
	if validChannel == False:
		raise ValueError('Channel does not exist')
	# Access Error when:
	# The authorised user is not a member of the channel that the message is within
	for mem in currentChannel['member']:
		if login_user['u_id'] == mem['u_id']:
			login_user['authorised'] == True
	if user['authorised'] == False:
		AccessError('User is not a member of channel')

	# Finish after 15 mins
	time_finished = datetime.now()+ timedelta(minutes=15) 
	return dumps({
		time_finished
		})

@app.route("/standup/send", methods=['POST'])
def standup_send():
	global channel, user, login_user
	token = request.form.get('token')
	channel_id = request.form.get('channel_id')
	message = request.form.get('message')
	# ValueError when:
	# Channel (based on ID) does not exist
	validChannel = False
	for c in channel:
		if channel_id == c['channel_id']:
			validChannel = True
			currentChannel = c
	if validChannel == False:
		raise ValueError('Channel does not exist')

	# Message is more than 1000 characters
	if len(message) > 1000:
		raise ValueError('Message must be less than 1000 characters')
	
	# If the standup time has stopped
	time_finished = standup_start()
	if datetime.now() > time_finished:
		raise ValueError('An active standup is not currently running in this channel')
	
	# AccessError when:
	# The authorised user is not a member of the channel that the message is within
	for mem in currentChannel['member']:
		if login_user['u_id'] == mem['u_id']:
			login_user['authorised'] == True
	if user['authorised'] == False:
		AccessError('User is not a member of channel')

	# Sending a message to get buffered in the standup queue
	message_send(token, channel_id, message)

	return dumps({})
	
@app.route("/search", methods=['GET'])
def search():
	global messages
	token = request.args.get('token')
	query = request.args.get('query_str')
	# No Exception
	# Given a query string, return a collection of messages in all of the channels 
	# that the user has joined that match the query
	matching_message = []
	for mes in messages:
		if query in mes['message']:
			matching_message.append(mes)

	return dumps({
		matching_message
		})

@app.route("/admin/userpermission/change", methods=['POST'])
def admin_userpermission_change():
	global user, login_user
	token = request.form.get('token')
	u_id = request.form.get('u_id')
	permission_id = request.form.get('permission_id')

	# 1) Check whether the authorised user is Admin or Owner
	if login_user['permission_id'] is not 'Admin':
		if login_user['permission_id'] is not 'Owner':
			AccessError("Access Denied")
	# 2) Check whether u_id is valid
	valid = False
	for u in user:
		if u_id == u['u_id']:
			valid = True
			break
	if valid == False:
		raise ValueError("Invalid user ID")
	# 3) Check whether permission_id refers to a value permission
	if permission_id is not 'Admin':
		if permission_id is not 'Owner':
			raise ValueError("Invalid Permission ID")
	# If passed every test, set u_id to new permission_id
	u['u_id'] = permission_id

	return dumps({})
	

if __name__ == "__main__":
	app.run(debug=True)


