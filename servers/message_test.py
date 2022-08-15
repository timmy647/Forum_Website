import pytest
from message import*
from message import AccessError

'''
This file is the test function of the Project - Iteration , from message_remove to user_profile
written by Zoe Li - M13A-FZY
'''
def message_remove (token, message_id)
    target_message_token = 12345 # The message is sent by the person with token 12345
    owner_token = 67890 #the owner's token of the channel/slack
    if message_id == 'notexist':
        raise ValueError('Message does not exists')   
    elif token != target_message_token
        raise AssessError('Not sent by the authorised user')  
    elif token != owner_token
        raise AssessError('No permission')  
    pass

def test_message_remove ()
    # SETUP_START
    # Register members
    u_id1, token1 = auth_register('zoe@FZY.com' ,'zoe123','Zoe', 'Li')
    u_id2, token2 = auth_register('freya@FZY.com', 'freya123', 'Freya', 'Li')
    u_id3, token3 = auth_register('tim@FZY.com', 'tim123', 'Tim', 'Liu')
    # Create and join members in the channel
    channelIsCreate = channels_create(token1,'my_channel',True) # u_id1 is the owner of channel1
    channel1 = channelIsCreate["channel_id"]
    channel_join(token1, channel1)
    channel_join(token2, channel1)
    channel_join(token3, channel1)
    # Send messages
    message_send(token1, channel1, 'Hello') # Assume the message_id of this message is 1
    message_send(token1, channel1, 'How is it going?') # Assume the message_id of this message is 2
    message_send(token2, channel1, 'Allg') # Assume the message_id of this message is 3
    message_send(token3, channel1, 'XD') # Assume the message_id of this message is 4
    # SETUP_END

    message_remove (token1, 1)
    with pytest.raises(ValueError, match=r"*"): # Message (based on ID) no longer exists
        message_remove (token1, 6)
    with pytest.raises(AccessError, match=r"*"): # Message with message_id was not sent by an owner of this channel
        message_remove (token2, 1)
    with pytest.raises(AccessError, match=r"*"): # Message with message_id was not sent by the authorised user making this request
        message_remove (token3, 3)




def message_edit (token, message_id, message)
    target_message_token = 12345 # The message is sent by the person with token 12345
    owner_token = 67890 #the owner's token of the channel/slack
    if token != message_token
        raise ValueError('Message does not exists')   
    elif token != target_message_token
        raise ValueError('Not sent by the authorised user')  
    elif token != owner_token
        raise ValueError('No permission')  
    pass

def test_message_edit (token, message_id, message)
    # SETUP_START
    # Register members
    u_id1, token1 = auth_register('zoe@FZY.com' ,'zoe123','Zoe', 'Li')
    u_id2, token2 = auth_register('freya@FZY.com', 'freya123', 'Freya', 'Li')
    u_id3, token3 = auth_register('tim@FZY.com', 'tim123', 'Tim', 'Liu')
    # Create and join members in the channel
    channelIsCreate = channels_create(token1,'my_channel',True) # u_id1 is the owner of channel1
    channel1 = channelIsCreate["channel_id"]
    channel_join(token1, channel1)
    channel_join(token2, channel1)
    channel_join(token3, channel1)
    # Send messages
    message_send(token1, channel1, 'Hello') # Assume the message_id of this message is 1
    message_send(token1, channel1, 'How is it going?') # Assume the message_id of this message is 2
    message_send(token2, channel1, 'Allg') # Assume the message_id of this message is 3
    message_send(token3, channel1, 'XD') # Assume the message_id of this message is 4
    # SETUP_END

    message_edit(token1, 1, 'Hi!')
    with pytest.raises(ValueError, match=r"*"): # Message with message_id was not sent by the authorised user making this request
        message_edit (token3, 3, 'Its bad')
    with pytest.raises(ValueError, match=r"*"): # Message with message_id was not sent by an owner of this channel
        message_edit (token3, 1, 'Ewww..')
    



def message_react (token, message_id, react_id)
    react_id == 3 # Assume message_id already reacted with react_id 3
    if message_id == '5'
        raise ValueError('Not a valid message_id') 
    elif react_id == 99999
        raise ValueError('Not a valid react_id') 
    elif react_id == 3
        raise ValueError('Already reacted!') 
    pass

def test_message_react (token, message_id, react_id)
    #SETUP_START
    # Register members
    u_id1, token1 = auth_register('zoe@FZY.com' ,'zoe123','Zoe', 'Li')
    u_id2, token2 = auth_register('freya@FZY.com', 'freya123', 'Freya', 'Li')
    u_id3, token3 = auth_register('tim@FZY.com', 'tim123', 'Tim', 'Liu')
    u_id4, token4 = auth_register('yura@FZY.com', 'yura123', 'Yura', 'Bae')
    # Create and join members in the channel
    channelIsCreate = channels_create(token1,'my_channel',True) # u_id1 is the owner of channel1
    channel1 = channelIsCreate["channel_id"]
    channelIsCreate = channels_create(token3,'a_channel',True) # u_id3 is the owner of channel3
    channel1 = channelIsCreate["channel_id"]
    channel_join(token1, channel1)
    channel_join(token2, channel1)
    channel_join(token3, channel2)
    channel_join(token4, channel2)
    # Send messages
    message_send(token1, channel1, 'Hello') # Assume the message_id of this message is 1
    message_send(token2, channel1, 'How is it going?') # Assume the message_id of this message is 2
    message_send(token3, channel2, 'Allg') # Assume the message_id of this message is 3
    message_send(token4, channel2, 'XD') # Assume the message_id of this message is 4
    # Make a reaction (Assume react_id is from 1-100)
    message_react(token2, 1, 1)
    # SETUP_END

    message_react(token1, 1, 1)
    with pytest.raises(ValueError, match=r"*"): # message_id is not a valid message within a channel that the authorised user has joined
        message_react(token1, 3, 1)
    with pytest.raises(ValueError, match=r"*"): # react_id is not a valid React ID
        message_react(token4, 3, 'a')
    with pytest.raises(ValueError, match=r"*"): # Message with ID message_id already contains an active React with ID react_id
        message_react(token2, 1, 1)





def message_unreact (token, message_id, react_id)
    react_id == 3 # Assume message_id already reacted with react_id 3
    if message_id == '5'
        raise ValueError('Not a valid message_id') 
    elif react_id == 99999
        raise ValueError('Not a valid react_id') 
    elif react_id == 2
        raise ValueError('No ceritain reaction')
    pass

def test_message_unreact (token, message_id, react_id)
   # SETUP_START
    # Register members
    u_id1, token1 = auth_register('zoe@FZY.com' ,'zoe123','Zoe', 'Li')
    u_id2, token2 = auth_register('freya@FZY.com', 'freya123', 'Freya', 'Li')
    u_id3, token3 = auth_register('tim@FZY.com', 'tim123', 'Tim', 'Liu')
    # Create and join members in the channel
    channelIsCreate = channels_create(token1,'my_channel',True) # u_id1 is the owner of channel1
    channel1 = channelIsCreate["channel_id"]
    channel_join(token1, channel1)
    channel_join(token2, channel1)
    channel_join(token3, channel1)
    # Send messages
    message_send(token1, channel1, 'Hello') # Assume the message_id of this message is 1
    message_send(token1, channel1, 'How is it going?') # Assume the message_id of this message is 2
    message_send(token2, channel1, 'Allg') # Assume the message_id of this message is 3
    message_send(token3, channel1, 'XD') # Assume the message_id of this message is 4
    # SETUP_END

    message_edit(token1, 1, 'Hi!')
    with pytest.raises(ValueError, match=r"*"): # Message with message_id was not sent by the authorised user making this request
        message_edit (token3, 3, 'Its bad')
    with pytest.raises(ValueError, match=r"*"): # Message with message_id was not sent by an owner of this channel
        message_edit (token3, 1, 'Ewww..')
    



def message_pin (token, message_id)
    admin_token = 12345
    pinned_message_id = 67890
    channel_member = [1,2,3]
    if message_id == 'notexist':
        raise ValueError('Message does not exists')  
    elif token != admin_token
        raise ValueError('No permission')
    elif message_id == pinned_message_id
        raise ValueError('Already pinned')
    elif token not in channel_member
        raise AssessError('Not in channel') 
    pass

def test_message_pin (token, message_id)
    #SETUP_START
    # Register members
    u_id1, token1 = auth_register('zoe@FZY.com' ,'zoe123','Zoe', 'Li')
    u_id2, token2 = auth_register('freya@FZY.com', 'freya123', 'Freya', 'Li')
    u_id3, token3 = auth_register('tim@FZY.com', 'tim123', 'Tim', 'Liu')
    admin_userpermission_change(token1, u_id1, 2) # set as admin (permission_id 2)
    # Create and join members in the channel
    channelIsCreate = channels_create(token1,'my_channel',True) # u_id1 is the owner of channel1
    channel1 = channelIsCreate["channel_id"]
    channel_join(token1, channel1)
    channel_join(token2, channel1)
    # Send messages
    message_send(token1, channel1, 'Hello') # Assume the message_id of this message is 1
    message_send(token2, channel1, 'How is it going?') # Assume the message_id of this message is 2
    message_send(token3, channel2, 'Allg') # Assume the message_id of this message is 3
    message_send(token4, channel2, 'XD') # Assume the message_id of this message is 4

    # SETUP_END
    message_pin (token1, 1)
    with pytest.raises(ValueError, match=r"*"): # Message_id is not a valid message
        message_pin (token1, 999)
    with pytest.raises(ValueError, match=r"*"): # The authorised user is not an admin
        message_pin (token2, 2)
    with pytest.raises(ValueError, match=r"*"): # Message with ID message_id is already pinned
        message_pin (token1, 1)
    with pytest.raises(AccessError, match=r"*"): # The authorised user is not a member of the channel that the message is within
        message_pin (token3, 3)




def message_unpin (token, message_id)
    admin_token = 12345
    unpinned_message_id = 67890
    channel_member == [1,2,3]
    if message_id == 'notexist':
        raise ValueError('Message does not exists')  
    elif token != admin_token
        raise ValueError('No permission')
    elif message_id == unpinned_message_id
        raise ValueError('Message is not pinned')
    elif token not in channel_member
        raise AssessError('Not in channel') 
    pass

def test_message_unpin (token, message_id)
    #SETUP_START
    # Register members
    u_id1, token1 = auth_register('zoe@FZY.com' ,'zoe123','Zoe', 'Li')
    u_id2, token2 = auth_register('freya@FZY.com', 'freya123', 'Freya', 'Li')
    u_id3, token3 = auth_register('tim@FZY.com', 'tim123', 'Tim', 'Liu')
    admin_userpermission_change(token1, u_id1, 2) # set as admin (permission_id 2)
    # Create and join members in the channel
    channelIsCreate = channels_create(token1,'my_channel',True) # u_id1 is the owner of channel1
    channel1 = channelIsCreate["channel_id"]
    channel_join(token1, channel1)
    channel_join(token2, channel1)
    # Send messages
    message_send(token1, channel1, 'Hello') # Assume the message_id of this message is 1
    message_send(token2, channel1, 'How is it going?') # Assume the message_id of this message is 2
    message_send(token3, channel2, 'Allg') # Assume the message_id of this message is 3
    message_send(token4, channel2, 'XD') # Assume the message_id of this message is 4
    # Pin messages
    message_pin (token1, 1)
    message_pin (token1, 2)
    message_pin (token1, 3)
    message_pin (token1, 4)
    # SETUP_END

    message_unpin (token1, 1)
    with pytest.raises(ValueError, match=r"*"): # Message_id is not a valid message
        message_unpin (token1, 999)
    with pytest.raises(ValueError, match=r"*"): # The authorised user is not an admin
        message_unpin (token2, 2)
    with pytest.raises(ValueError, match=r"*"): # Message with ID message_id is already pinned
        message_unpin (token1, 3)
    with pytest.raises(AccessError, match=r"*"): # The authorised user is not a member of the channel that the message is within
        message_unpin (token3, 4)




def user_profile (token, u_id) 
    if token == 'unknown'
        raise ValueError('Member does not exists') 
    return {
         'yura@FZY.com', 'yura123', 'Yura', 'Bae'
    }

def test_user_profile (token, u_id) 
    #SETUP_START
    # Register member
    u_id4, token4 = auth_register('yura@FZY.com', 'yura123', 'Yura', 'Bae')
    # SETUP_END

    user_profile (token4, u_id4)
    
    with pytest.raises(ValueError, match=r"*"): # Message_id is not a valid message
        user_profile (token0, u_id0)