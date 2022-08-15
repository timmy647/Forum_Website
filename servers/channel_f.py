from error import AccessError
from json import dumps
from flask import Flask, request
import jwt
import os
import pickle
import uuid
from flask_mail import Mail, Message
import sys
import uuid
import time

###-------------------------channel_function----------------------------###
user = [{}]
channel = [{}]


def save():
    global user, channel
    with open('userStore.p', 'wb') as FILE:
        pickle.dump(user, FILE)
    with open('channelStore.p', 'wb') as FILE:
        pickle.dump(channel, FILE)

def get_channel_id():
    return uuid.uuid4().int>>80

message_id = 0
def get_message_id():
    global message_id
    if os.path.getsize('messageIDStore.p') > 0:
        message_id = pickle.load(open('messageIDStore.p', 'rb'))
    message_id += 1
    with open('messageIDStore.p', 'wb') as FILE:
        pickle.dump(message_id, FILE)
    return message_id

def save_user():
    global user
    with open('userStore.p', 'wb') as FILE:
        pickle.dump(user, FILE)  

def save_channel():  
    global channel   
    with open('channelStore.p', 'wb') as FILE:
        pickle.dump(channel, FILE)

def load_user():
    global user
    if os.path.getsize('userStore.p') > 0:
        with open('userStore.p','rb') as save_user:
            user = pickle.load(save_user)
            return user
    else:
        return []

def load_channel():
    global channel
    if os.path.getsize('channelStore.p') > 0:
        with open('channelStore.p','rb') as save_channel:
            channel = pickle.load(save_channel) 
            return channel
    else:
        return []


def channel_invite(channel_id, u_id, token):
    global user, channel
    user = pickle.load(open('userStore.p', 'rb'))
    channel = pickle.load(open('channelStore.p', 'rb'))

    channel_id = int(channel_id)
    u_id = int(u_id)
    token = str(token)

    user_found = 0
    for u in user:
        if u_id == u['u_id']:
            user_found = 1
    if user_found == 0:
        raise ValueError("Invalid user ID")

    channel_found = 0
    for c in channel:
        if channel_id == c['channel_id']:
            channel_found = 1
            channel_name = c['name']
    if channel_found == 0:
        raise ValueError("Invalid channel ID")

    auth = 0
    for u in user:
        if u['token'] == token:
            for ch_list in u['channel_list']:
                if channel_id == ch_list['channel_id']:
                    auth = 1

    if auth == 0:
        raise ValueError("The authorised user is not already a member of the channel")

    for u in user:
        if u_id == u['u_id']:
            dic ={
                'channel_id': channel_id,
                'name': channel_name,
                'permission': 3,
            }
            u['channel_list'].append(dic)

    for c in channel:
        if channel_id == c['channel_id']:
            c['member'].append(u_id)
    save()
    return dumps({})


def channel_details(channel_id, token):
    global user, channel
    user = pickle.load(open('userStore.p', 'rb'))
    channel = pickle.load(open('channelStore.p', 'rb'))

    for u in user:
        if u['token'] == token:
            u_id = u['u_id']

    channel_found = 0
    owners = []
    members = []
    for c in channel:
        if int(channel_id) == c['channel_id']:
            channel_found = 1
            channel_name = c['name']
            channel_owner = c['owner']
            channel_member = c['member']
            # if u_id not in channel_member:
            #     raise ValueError("Not a member of the channel")

            for o in c['owner']:
                for u in user:
                    if o == u['u_id']:
                        dic = {
                            'u_id': int(u['u_id']),
                            'name_first': str(u['name_first']),
                            'name_last': str(u['name_last']),
                            'profile_img_url': '',
                        }
                        owners.append(dic)
            for m in c['member']:
                for u in user:
                    if m == u['u_id']:
                        dic = {
                            'u_id': int(u['u_id']),
                            'name_first': str(u['name_first']),
                            'name_last': str(u['name_last']),
                            'profile_img_url': '',
                        }
                        members.append(dic)

    if channel_found == 0:
        raise ValueError("Invalid channel ID")

    return dumps({
        "name": channel_name,
        "owner_members": owners,
        "all_members": members,
    })


def channel_messages(token, channel_id, start):
    global user, channel
    user = pickle.load(open('userStore.p', 'rb'))
    channel = pickle.load(open('channelStore.p', 'rb'))

    for u in user:
        if u['token'] == token:
            u_id = u['u_id']

    start = int(start)
    channel_found = 0
    end = 0
    for c in channel:
        if int(channel_id) == c['channel_id']:
            channel_found = 1
            if start > len(c['message']):
                raise ValueError("Start is greater than the toal number of messages")
            messages = []
            channel_members = c['member']
            if u_id not in channel_members:
                raise ValueError("Not a member of the channel")

            if len(c['message']) - start >= 50:
                end = start + 50
                length = 50
            else:
                end = -1
                length = len(c['message']) - start
            if len(c['message']) != 0:
                for i in range(0, (length)):
                    tmp = c['message'][start + i]
                    messages.append(tmp)

    if channel_found == 0:
        raise ValueError("Invalid channel ID")

    print(messages)
    return dumps({
        'messages': messages,
        'start': start,
        'end': end,
    })


def channel_leave(token,channel_id):
    global channel, user
    user = pickle.load(open('userStore.p', 'rb'))
    channel = pickle.load(open('channelStore.p', 'rb'))

    channel_user = False
    channel_id = int(channel_id)
    for u in user:
        if token == u['token']:
            u_id = u['u_id']
            for item in u['channel_list']:
                if channel_id == item['channel_id']:
                    channel_user = True
            break        

    if channel_user == False:
        raise AccessError('The authorised user has not joined the channel')

    have_channel = False        
    for c in channel: 
        if channel_id == c['channel_id']: # channel exist
            have_channel = True
            c['member'].remove(u_id)
            for i in u['channel_list']:
                if channel_id == i['channel_id']:
                    u['channel_list'].remove(i)
            # remove the channel_id from the channels of user     
    if have_channel == False:  
        raise ValueError("Channel ID is not a valid channel") 

    save_channel()
    save_user()
    return dumps({})

 
def channel_join(token, channel_id):
    global channel, user
    user = pickle.load(open('userStore.p', 'rb'))
    channel = pickle.load(open('channelStore.p', 'rb'))

    for u in user: # search user
        if token == u['token']: # find user
            u_id = u['u_id']
            break
    
    have_channel = False
    channel_id = int(channel_id)
    for c in channel:
        if channel_id == c['channel_id']: #channel exist
            have_channel = True
            if c['is_public'] == True: # public channel
                c['member'].append(u_id)  # append the u_id in member list 
                dic = {
                    'channel_id': channel_id,
                    'name': c['name'],
                    'permission': 2
                }       
                u['channel_list'].append(dic) # append the channel_id in the channel list of user
                
            else: # not public channel
                if u_id in c['owner']: # user is owner
                    c['member'].append(u_id)  # append the u_id in member list        
                else:    
                    raise AccessError("channel is private") 
            break

    if have_channel == False:        
        raise ValueError("Channel ID is not a valid channel")

    save_user()
    save_channel()

    return dumps({})

def channel_addowner(token,channel_id,u_id):
    global channel, user
    user = pickle.load(open('userStore.p', 'rb'))
    channel = pickle.load(open('channelStore.p', 'rb'))
   
    channel_user = False
    token = str(token)
    channel_id = int(channel_id)
    u_id = int(u_id)
    for u in user:
        if token == u['token']:
            authorised = u['u_id'] # user1
            for item in u['channel_list']:
                if channel_id == item['channel_id']:
                    channel_user = True    
            break           
                
    if channel_user == False:
        raise AccessError('The authorised user has not joined the channel')

    have_channel = False
    for c in channel:
    # search all channel
        if channel_id == c['channel_id']: 
            have_channel = True     
            if authorised in c['owner']: # authorised user not an onwen of channel
                if u_id not in c['owner']: # user is not the owner
                    c['owner'].append(u_id)
                else:
                    raise ValueError("user is already the owner")                           
            else: 
                raise AccessError("The authorised user is not an owner")  
                   
    if have_channel == False:
       raise ValueError("Channel ID is not a valid channel")
    save_channel()
    save_user()                           
    return dumps({})

def channel_removeowner(token,channel_id,u_id):
    global channel, user
    user = pickle.load(open('userStore.p', 'rb'))
    channel = pickle.load(open('channelStore.p', 'rb'))

    have_channel = False
    token = str(token)
    channel_id = int(channel_id)
    u_id = int(u_id)
    
    for c in channel:
    # search all channel
        if channel_id == c['channel_id']:# channel exist
            have_channel = True
            for u in user: 
                if token == u['token']: # find user 
                    authorised = u['u_id']      
                    if authorised not in c['owner']:
                    # authorised user not an onwen of slacker or channel
                        raise AccessError("The authorised user is not an owner")               
                    else:
                        if u_id not in c['owner']: # user is not the owner
                            raise ValueError("user is not the owner") 
                        else:   
                            c['owner'].remove(u_id)   
    if have_channel == False:       
            raise ValueError("Channel ID is not a valid channel")

    save_channel()
    save_user()   
    return dumps({})

def channels_list(token):
    global user
    user = load_user()
    channels = []
    for u in user:
        if token == u['token']:
            if len(u['channel_list']) != 0:
                for ch in u['channel_list']:
                    
                    dic = {
                        'channel_id': ch['channel_id'],
                        'name': ch['name']
                    }                
                    channels.append(dic)
            break 
    return dumps({
        'channels': channels
    })

def channels_listall(token):
    global channel
    channel = load_channel()
    

    channels = []
    if len(channel) != 0:
        for c in channel:
            dic = {
                'channel_id': c['channel_id'],
                'name': c['name']
            }
            channels.append(dic)
    return dumps({
        'channels':channels
    })

def channels_create(token,name,is_public):
    global channel, user
    user = pickle.load(open('userStore.p', 'rb'))
    channel = pickle.load(open('channelStore.p', 'rb'))

    if is_public == "false":
        is_public = False
    else:
        is_public = True
      
    name = str(name)
    if len(name) > 20:
        raise ValueError("Name is more than 20 characters long")
    
    channel_id = get_channel_id()
    for u in user: 
        if token == u['token']:
            u_id = u['u_id'] 
            break
    
    dic = {
        'name': name,
        'channel_id': channel_id,
        'owner': [],
        'member':[],
        'is_public': is_public,
        'message':[] 
    }
    dic['owner'].append(u_id)
    dic['member'].append(u_id)  
    dic2 = {
        'channel_id': channel_id,
        'name': name,
        'permission': 1
    }
    channel.append(dic)
    u['channel_list'].append(dic2)
    save_channel()
    save_user() 
    return dumps({
        'channel_id': channel_id
    })

def message_sendlater(token,channel_id,message,time_sent):
    global channel, user
    user = pickle.load(open('userStore.p', 'rb'))
    channel = pickle.load(open('channelStore.p', 'rb'))
    
    if len(message) > 1000:
        raise ValueError('Message is more than 1000 characters')

    if time_sent < datetime.datetime.utcnow().timestamp():
        raise ValueError('Time sent is a time in the past')

    channel_user = False
    for u in user:
        if token == u['token']:
            u_id = u['u_id']
            for item in u['channel_list']:
                if channel_id == item['channel_id']:
                    channel_user = True
            break 
    if channel_user == False:
        raise AccessError('The authorised user has not joined the channel')

    message_id = get_message_id()
    have_channel = False
    
    for c in channel:
        if channel_id == c['channel_id']:# channel exist 
            have_channel = True  

            dic = {
                'message': message,
                'message_id': message_id, 
                'u_id': u_id, 
                'time_sent': time_sent,
                'reacts': [{
                    'react_id': 1,
                    'u_ids': [],
                    'is_this_user_reacted': False
                }],
                'time_created': datetime.datetime.utcnow().timestamp(),
                'is_pinned': False                          
            }
            c['message'].append(dic) 
            break                      
                          
    if have_channel == False:
        raise ValueError("Channel ID is not a valid channel")

    save_channel()
    save_user() 

    return dumps({
        'message_id': message_id
    })


def message_send(token,channel_id,message):
    global channel, user 
    user = pickle.load(open('userStore.p', 'rb'))
    channel = pickle.load(open('channelStore.p', 'rb'))

    if len(message) > 1000:
        raise ValueError('Message is more than 1000 characters')

    channel_user = False
    channel_id = int(channel_id)
    for u in user:
        if token == u['token']:
            u_id = u['u_id']
            for item in u['channel_list']:
                if channel_id == item['channel_id']:
                    channel_user = True
            break
                
    if channel_user == False:
        raise AccessError('The authorised user has not joined the channel')

    message_id = get_message_id()
    have_channel = False
    for c in channel:
        if channel_id == c['channel_id']:# channel exist 
            have_channel = True         
            now = int(time.time())
            dic = {
                'message_id': int(message_id),
                'u_id': int(u_id),
                'message': str(message),
                'time_created': int(now),
                'reacts': [],
                'is_pinned': False,
            }
            c['message'].append(dic) 
            
            break                      

    if have_channel == False:
        raise ValueError("Channel ID is not a valid channel")

    save_channel()
    save_user() 

    return dumps({
        'message_id': message_id
    })
