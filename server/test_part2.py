
from json import dumps
from flask import Flask, request, jsonify
from Error import AccessError
import jwt
import sys
import datetime
import uuid

APP = Flask(__name__)



channel = [{
    'name':'',
    'channel_id':'',
    'is_public': False, 
    'owner':[], # owner of the channel or slackr
    'member':[],
    'message' : [{
        'message' :'',
        'message_id':'',
        'user':'',
        'time_sent':'',
        'react_id':[],
        'pin': False
    }]
}]

user = {
    'email': '',
    'password':'',
    'u_id':'',
    'token':'',
    'login': False 
    'permission_id':'' # slackr
    'channel_list':[{
        'channel_id':'
        'permission':'' # channel
    }]
}


# get u_id
u_id = 0
def get_uid(): # get unique u_id
    global u_id
    u_id = u_id + 1
    return u_id
   
@APP.route('/channel/leave', methods=['POST'])
def channel_leave():
    global channel, user
    decode = jwt.decode(token, 'activate', algorithms=['HS256'])
    channel_id = request.form.get['channel_id']
    token = request.form.get['token']
    # imfortation

    for c in channel: 
        if channel_id not in c['channel_id']: # channel not exist
            raise ValueError("Channel ID is not a valid channel")
        else: # channel exist
            for u in user: 
                if token == u['token'] # find the user
                    u_id == u['u_id']
                    u['member'].remove(u_id)  
                    u['channel_list'].remove(channel_id) 
                    # remove the channel_id from the channels of user       
    return dumps({})


@APP.route('/channel/join', methods=['POST'])
def channel_join():
    global channel, user
    decode = jwt.decode(token, 'activate', algorithms=['HS256'])
    channel_id = request.form.get['channel_id']
    token = request.form.get['token']
    # imfortation

    for c in channel:
        if channel_id not in c['channel_id']: #channel exist
            raise ValueError("Channel ID is not a valid channel")
        else:
            for u in user: # search user
                if token == u['token']: # find user
                    if c['is_public'] == False # not a public channel
                        if u['permission_id'] != 3: # user is not the admin of slackr
                            raise AccessError("The authorised user is not an admin")
                        else: # user is the admin of slackr
                            u_id == u['u_id'] 
                            c['owner'].append(u_id)  
                            # append the u_id in member list        
                            u['channel_list'].append(channel_id) 
                    else: # public channel  
                        u_id == u['u_id'] 
                        c['member'].append(u_id)  
                        # append the u_id in member list        
                        u['channel_list'].append(channel_id) 
                        # append the channel_id in the channel list of user    
    return dumps({})

@APP.route('/channel/addowner', methods=['POST'])
def channel_addowner():
    global channel, user
    decode = jwt.decode(token, 'activate', algorithms=['HS256'])
    token = request.form.get['token']
    u_id = request.form.get['u_id'] # user 
    channel_id = request.form.get['channel_id']

    for c in channel:
    # search all channel
        if channel_id not in c['channel_id']: # channel not exist
            raise ValueError("Channel ID is not a valid channel")
        else: # channel exist
            for u in user: 
                if token == u['token']: # find user 
                    authorised = u['u_id']      
                    if authorised not in c['owner'] or u['permission_id'] == 3:
                    # authorised user not an onwen of slacker or channel
                        raise AccessError("The authorised user is not an owner")               
                    else:
                        if u_id in c['owner']: # user is not the owner
                            raise ValueError("user is already the owner") 
                        else:   
                            c['owner'].append(u_id) 
                                
    return dumps({})

@APP.route('/channel/removeowner', methods=['POST'])
def channel_removeowner():
    global channel, user
    decode = jwt.decode(token, 'activate', algorithms=['HS256'])
    token = request.form.get['token']
    u_id = request.form.get['u_id']
    channel_id = request.form.get['channel_id']
    # get information

    for c in channel:
    # search all channel
        if channel_id not in c['channel_id']:# channel exist
            raise ValueError("Channel ID is not a valid channel")
         else: # channel exist
            for u in user: 
                if token == u['token']: # find user 
                    authorised = u['u_id']      
                    if authorised not in c['owner'] or u['permission_id'] == 3:
                    # authorised user not an onwen of slacker or channel
                        raise AccessError("The authorised user is not an owner")               
                    else:
                        if u_id not in c['owner']: # user is not the owner
                            raise ValueError("user is not the owner") 
                        else:   
                            c['owner'].remove(u_id)    
    return dumps({})

@APP.route('/channels/list', methods=['GET'])
def channels_list():
    global user, channel
    token = request.args.get['token']
    for u in user:
        if token == u['token']:
            channels_list == u['channel_list']
    return dumps({
        'channels': channel_list
    })

@APP.route('/channels/listall', methods=['GET'])
def channels_listall():
    global user, channel

    return dumps({
        'name':'',
        'channel_id':'',
    })

@APP.route('/channels/create', methods=['POST'])
def channels_create():
    global channel, user
    decode = jwt.decode(token, 'activate', algorithms=['HS256'])
    name = request.form.get['name']
    token = request.form.get['token']
    is_public = request.form.get['is_public']
    # get information
    
    if len(name) > 20:
        raise ValueError("Name is more than 20 characters long")
    else:  
        channel_id = uuid.uuid1().int 
        for u in user:
            if token == u['token']:
                u_id == u['u_id']
                dic2 = {
                    'channel_id': channel_id,
                    'permission': 1
                }
        
        dic = {
            'name': name,
            'channel_id': channel_id
            'owner': u_id
            'is_public': is_public       
        }   
        channel.append(dic)
        
    return dumps({
        'channel_id': channel_id
    })

@APP.route('/channel/sendlater', methods=['POST'])
def message_sendlater():
    global channel, user, message
    channel_id = request.form.get['channel_id']
    message = request.form.get['message']
    # get information
    
    for c in all_channel:
        if channel_id == c['channel_id']:# channel exist           
            if len(message) > 1000:
                raise ValueError('Message is more than 1000 characters')         
            if channel_id in login_user['channel_list']:
                raise AccessError('The authorised user has not joined the channel')
            if message['time_sent'] < datetime.datetime.now:
                raise ValueError('Time sent is a time in the past')
        else:
            raise ValueError("Channel ID is not a valid channel")
    return dumps({
        'message_id':''
    })

@APP.route('/channel/send', methods=['POST'])
def message_send():
    global channel, user, message
    decode = jwt.decode(token, 'activate', algorithms=['HS256'])
    token = request.form.get['token']
    channel_id = request.form.get['channel_id']
    message = request.form.get['message']
    # get information

    for c in channel:
        if channel_id not in c['channel_id']:# channel exist 
            raise ValueError("Channel ID is not a valid channel")
        else: 
            for u in user:

                if len(message) > 1000:
                    raise ValueError('Message is more than 1000 characters')         
                if channel_id not in u['channel_list']:
                    raise AccessError('The authorised user has not joined the channel')
            
    return dumps({
        'message_id':''
    })
    
    
if __name__ == '__main__':
    APP.run(port=(sys.argv[1] if len(sys.argv) > 1 else 5000))
