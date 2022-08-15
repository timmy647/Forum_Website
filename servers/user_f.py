
from validemail import check
from error import AccessError
from datetime import datetime, timedelta

emailList = {'exist@email.com'}
channelDict = {'channel_id':[123], 'name':['existChannel']}

auth_u_id = [12345]
permissionID = [123456789]

admin_token = "ADMIN"
owner_token = "OWNER"

def user_profile_setname(token, name_first, name_last):
	# ValueError when:
	# name_first is more than 50 characters
	if len(name_first) > 50:
		raise ValueError('First name must be less than 50 characters')
	# name_last is more than 50 characters
	elif len(name_last) > 50:
		raise ValueError('Last name must be less than 50 characters')

def user_profile_setemail(token, email):
	# Email entered is not a valid email
	if not check(email)=='Valid Email':
		raise ValueError('Invalid Email')
	# Email address is already being used by another user
	elif email in emailList:
		raise ValueError('Email already registered')
	# Update the authorised user's email address

def user_profile_sethandle(token, handle_str):
	# Value Error when:
	# handle_str is no more than 20 characters
	if len(handle_str) <= 20:
		raise ValueError('Handle must be more than 20 characters')

def user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end, y_end):
	pass

def standup_start(token, channel_id):
	# Value Error when:
	# Channel (based on ID) does not exist
	if channel_id not in channelDict['channel_id']:
		raise ValueError('Channel does not exist')

	# Access Error when:
	# The authorised user is not a member of the channel that the message is within
	elif token != 'Valid Token':
		raise AccessError('User is not a member of channel')

	# Finish after 15 mins
	time_finished = datetime.now()+ timedelta(minutes=15) 
	return time_finished

def standup_send(token, channel_id, message):
	# ValueError when:
	# Channel (based on ID) does not exist
	if channel_id not in channelDict['channel_id']:
		raise ValueError('Channel does not exist')

	# Message is more than 1000 characters
	elif len(message) > 1000:
		raise ValueError('Message must be less than 1000 characters')

	# AccessError when:
	# The authorised user is not a member of the channel that the message is within
	elif token != 'Valid Token':
		raise AccessError('User is not a member of channel')
	# If the standup time has stopped
	

def search(token, query_str):
	# No Exception
	matching_message = "Valid message"
	return matching_message

def admin_userpermission_change(token, u_id, permission_id):
	# ValueError when:
	# u_id does not refer to a valid user
	if u_id not in auth_u_id:
		raise ValueError("Invalid user ID")

	# permission_id does not refer to a value permission
	elif permission_id not in permissionID:
		raise ValueError("Permission Denied")

	# AccessError when:
	# The authorised user is not an admin or owner
	elif (token != admin_token) and (token != owner_token):
		raise AccessError("Access Denied")

	

