Assumptions

Authorization
auth_login
    Assume a bad email means the email inserted is not in the format of xxx@xxx.com, or the email does not exists.
auth_logout
    Assume logout would quit all the channel this person has joined.
    Assume logout would not lose the permission of the slack/channel.
auth_register
    Assume a bad email means the email inserted is not in the format of xxx@xxx.com or the email does not exist.
    Assume two different users cannot have the same email.
    Assume a valid password means It needs to be at least 8 characters and a combination of letters and numbers.
auth_passwordreset_request
    Assume only the user himself could be able to reset the password
auth_passwordreset_reset
    Assume a valid password means It needs to be at least 8 characters and a combination of letters and numbers.
    
    
Channel
channel_invite
    Assume the authorized user could only invite when the user is in the channel.
channel_details
    Assume the owner of the slack who are not in the channel can view details of the channel.
channel_messages
    N/A
channel_leave
    Assume leave the channel would not lose the permission of the channel.
channel_join
    Assume the user cannot  join the same channel twice.
    Assume the first person joined the channel would automatically granted the owner.
channel_addowner  
	Assume the owner of slack who are not in this channel can add other members as owner.
	Assume the owner of slack who are not the owner of channel can add itself as owner.
	Assume same user can be an owner of two channels at the same time.
channel_removeowner
    Assume the owner of slack who are not in this channel can remove other owners.
channels_list
    Assume the owner of slack who are not in this channel can view the details of the channel.
channels_listall
    Assume user who are not in this channel can view the details of the channel.
channels_create
    Assume two channels could not have the same name.
    Assume same user could create two channels at the same time.
    
    
Message
message_sendlater
    Assume a person could only send one message later.
    Assume the timing message will not be sent after the channel is disbanded.
message_send
    Assume the message will not be sent after the channel is disbanded.
message_remove
    Assume the message is permanently removed.
message_edit
    Assume a message can be edit infinite times.
message_react
    Assume a react_id is a set of pre-installed emoji that can be posted in the dialogue box.
    Assume the same member could only react the message once, but one message could have multiple reacts.
message_unreact
    Assume only the person who reacts could unreact his own react.
message_pin
    Assume there could be only up to 3 pinned messages simultaneously exists.
    Assume the pinned message would be pinned at the very front and no longer be at the original place.
message_unpin
    Assume the unpinned message would go back to the original place.
    
    
User
user_profile
    N/A
user_profile_setname
    Assume members can change the name although its the same.
user_profile_setemail
    Assume members can change the email although its the same.
user_profile_sethandle
    Assume members can have the same handle.
user_profiles_uploadphoto
    Assume photo can be any format and any size.
    
    
    
Standup
standup_start
    Assume the time must be set to 15 minutes when the function is called .
standup_send
    Assume a standup is currently active.
    
    
Others
Search
    Assume can search in any length and search any phrase(including spaces)
admin_userpermission_change
    N/A

