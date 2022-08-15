from error import AccessError

auth_channel_id = [5,6]
auth_u_id = [123,456]

# Send a message from authorised_user to the channel 
# specified by channel_id automatically at a specified time in the future
def message_sendlater(token,channel_id,message,time_sent):
    if channel_id not in auth_channel_id:
        raise ValueError('channel do not exist')
    if len(message) > 1000:
        raise ValueError('Message is more than 1000 characters')
    if time_sent < datetime.datetime:
        raise ValueError('Time sent is a time in the past')
    pass

#Send a message from authorised_user to the channel specified by channel_id
def message_send(token,channel_id,message):
    if channel_id not in auth_channel_id:
        raise ValueError('channel do not exist')
    if len(message) > 1000:
        raise ValueError('Message is more than 1000 characters')
    pass
