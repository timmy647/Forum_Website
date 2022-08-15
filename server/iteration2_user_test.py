
import pytest
from error import AccessError
from iteration2_user_f import user_profile_setname, user_profile_setemail, user_profile_sethandle,\
user_profiles_uploadphoto, standup_start, standup_send, search, admin_userpermission_change
from iteration2_user_f import messages, channel, user, login_user


##=============test user_profile_setname=============##

def test_user_profile_setname():
	# SETUP BEGIN
	# Register member
	RegisterDict = auth_register("example@email.com", "password", "validname", "validname")
	token = RegisterDict['token']
	# SETUP END

	# Successful
	user_profile_setname(token, 'Good', 'Name')
	assert(login_user['first name'] = 'Good')
	assert(login_user['last name'] = 'Name')

	# name_first over 50 characters 
	with pytest.raises(ValueError, match=r'First name must be less than 50 characters'):
		user_profile_setname(token,
			'..................this name is long................',
			'last_name'
			)
	# name_last over 50 characters
	with pytest.raises(ValueError, match=r'Last name must be less than 50 characters'):
		user_profile_setname(token,
			'first_name',
			'..................this name is long................'
			)

##=============test user_profile_setemail=============##

def test_user_profile_setemail():
	# SETUP BEGIN
	# Register member
	RegisterDict = auth_register("example@email.com", "password", "validname", "validname")
	token = RegisterDict['token']
	# SETUP END

	# Successful
	user_profile_setemail(token, 'goodemail@email.com')
	assert(login_user['email'] = 'goodemail@email.com')

	# Invalid email test
	with pytest.raises(ValueError, match=r'Invalid Email'):
		user_profile_setemail(token,'not_valid_email.com')

	# Already registered email 
	with pytest.raises(ValueError, match=r'Email already registered'):
		user_profile_setemail(token,'exist@email.com')

##=============test user_profile_sethandle=============##

def test_user_profile_sethandle():
	# SETUP BEGIN
	# Register member
	RegisterDict = auth_register("example@email.com", "password", "validname", "validname")
	token = RegisterDict['token']
	# SETUP END

	# Successful
	user_profile_sethandle(token, 'haydensmith')
	assert(	login_user['handle'] = 'haydensmith')

	# handle_str less than 20 char
	with pytest.raises(ValueError, match=r'Handle must be betweeen 3 and 20 characters'):
		user_profile_sethandle(token,'this handle has more than 20 characters')

##=============test standup_start=============##

def test_stand_up_start():
	# SETUP BEGIN
	# Register member
	RegisterDict = auth_register("example@email.com", "password", "validname", "validname")
	token = RegisterDict['token']
	
	# Valid and invalid channel ID
	valid_channelID = 123
	invalid_channelID = 987
	# SETUP END

	# Successful
	standup_start('Valid Token', valid_channelID) 

	# Channel does not exist
	with pytest.raises(ValueError, match=r'Channel does not exist'):
		standup_start('Valid Token',invalid_channelID) 

	# User is not a member of the channel
	with pytest.raises(AccessError, match=r'User is not a member of channel'):
		standup_start('invalid token',valid_channelID) 

##=============test standup_send=============##

def test_stand_up_send():
	# SETUP BEGIN
	# Register member
	RegisterDict = auth_register("example@email.com", "password", "validname", "validname")
	token = RegisterDict['token']
	
	# Valid and invalid channel ID
	valid_channelID = 123
	invalid_channelID = 987
	# SETUP END

	# Successful
	standup_send('Valid Token', valid_channelID, 'short message') 

	# Channel does not exist
	with pytest.raises(ValueError, match=r'Channel does not exist'):
		standup_send('Valid Token', invalid_channelID, 'short message') 

	# Message over 1000 char
	with pytest.raises(ValueError, match=r'Message must be less than 1000 characters'):
		standup_send('Valid Token', valid_channelID, 
			'...................................... ...\
			...................................... ....\
			...........................................\
			...........................................\
			...........................................\
			...........................................\
			...........................................\
			...........................................\
			...........................................\
			...........................................\
			...........................................\
			...........................................\
			...............A very long message.........\
			...........................................\
			...................which has...............\
			...........................................\
			..................more than................\
			...........................................\
			................1000 characters............\
			...........................................\
			...........................................\
			...........................................\
			...........................................\
			...........................................\
			...........................................\
			...........................................\
			...........................................\
			...........................................\
			')

	# User is not a member of the channel
	with pytest.raises(AccessError, match=r'User is not a member of channel'):
		standup_send('invalid token', valid_channelID, 'short message') 

##=================test search=================##
def test_search():
	# SETUP BEGIN
	RegisterDict = auth_register("example@email.com", "password", "validname", "validname")
	token = RegisterDict['token']
	# SETUP END

	# Successful
	search(token, "Some query string")

	# No Exception!

##==========test admin_userpermission_change ==========##
def test_admin_userpermission_change():

	# SETUP BEGIN
	# Register member
	ownerDict = auth_register("owner@email.com", "ow123", "OWNER", "last")
	owner_token = ownerDict['token']
	adminDict = auth_register("admin@email.com", "ad123", "ADMIN", "name")
	admin_token = adminDict['token']

	valid_userID = 12345
	invalid_userID = 98765
	valid_permission = 123456789
	invalid_permission = 987654321
	# SETUP END

	# Successful
	admin_userpermission_change(admin_token, valid_userID, valid_permission) 
	admin_userpermission_change(owner_token, valid_userID, valid_permission) 

	# u_id does not refer to a valid user
	with pytest.raises(ValueError, match=r'Invalid user ID'):
		admin_userpermission_change(admin_token, invalid_userID, valid_permission)

	# permission_id does not refer to a value permission
	with pytest.raises(ValueError, match=r'Permission Denied'):
		admin_userpermission_change(owner_token, valid_userID, invalid_permission) 

	# The authorised user is not an admin or owner
	with pytest.raises(AccessError, match=r'Access Denied'):
		admin_userpermission_change(token, valid_userID, valid_permission) 



