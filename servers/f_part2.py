'''
from channel_leave to message_sendlater
Yiwei LI
'''
from json import dumps
import uuid
import datetime
import sys
from flask import Flask, request
from error import AccessError

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
    'login': False,
    'permission_id':'', # slackr
    'channel_list':[{
        'channel_id':''
    }]
}



u_id = 0
def get_uid(): # get unique u_id
    global u_id
    u_id = u_id + 1
    return u_id

@APP.route('/channel/leave', methods=['POST'])
def channel_leave():
    global channel, user
    channel_id = request.form.get['channel_id']
    token = request.form.get['token']
    # imfortation
    for chan in channel:
        if channel_id not in chan['channel_id']: # channel not exist
            raise ValueError("Channel ID is not a valid channel")
        else: # channel exist
            for u in user:
                if token == u['token']:
                    u_id == u['u_id']
                    u['member'].remove(u_id)
                    u['channel_list'].remove(channel_id)
                    # remove the channel_id from the channels of user
    return dumps({})

@APP.route('/channel/join', methods=['POST'])
def channel_join():
    global channel, user
    channel_id = request.form.get['channel_id']
    token = request.form.get['token']
    # imfortation

    for chan in channel:
        if channel_id not in chan['channel_id']: #channel exist
            raise ValueError("Channel ID is not a valid channel")
        else:
            for u in user: # search user
                if token == u['token']: # find user
                    if not chan['is_public']: # not a public channel
                        if u['permission_id'] != 3: # user is not the admin of slackr
                            raise AccessError("The authorised user is not an admin")
                        else: # user is the admin of slackr
                            u_id == u['u_id']
                            chan['owner'].append(u_id)
                            # append the u_id in member list
                            u['channel_list'].append(channel_id)
                    else: # public channel
                        u_id == u['u_id']
                        chan['member'].append(u_id)
                        # append the u_id in member list
                        u['channel_list'].append(channel_id)
                        # append the channel_id in the channel list of user
    return dumps({})

@APP.route('/channel/addowner', methods=['POST'])
def channel_addowner():
    global channel, user
    token = request.form.get['token']
    u_id = request.form.get['u_id'] # user
    channel_id = request.form.get['channel_id']

    for chan in channel:
    # search all channel
        if channel_id not in chan['channel_id']: # channel not exist
            raise ValueError("Channel ID is not a valid channel")
        else: # channel exist
            for u in user:
                if token == u['token']: # find user
                    authorised = u['u_id']
                    if authorised not in chan['owner'] or u['permission_id'] == 3:
                    # authorised user not an onwen of slacker or channel
                        raise AccessError("The authorised user is not an owner")
                    else:
                        if u_id in chan['owner']: # user is not the owner
                            raise ValueError("user is already the owner")
                        else:
                            chan['owner'].append(u_id)
    return dumps({})

@APP.route('/channel/removeowner', methods=['POST'])
def channel_removeowner():
    global channel, user
    token = request.form.get['token']
    u_id = request.form.get['u_id']
    channel_id = request.form.get['channel_id']
    # get information

    for chan in channel:
    # search all channel
        if channel_id not in c['channel_id']:# channel exist
            raise ValueError("Channel ID is not a valid channel")
        else:
            for u in user:
                if token == u['token']: # find user
                    authorised = u['u_id']
                    if authorised not in chan['owner'] or u['permission_id'] == 3:
                    # authorised user not an onwen of slacker or channel
                        raise AccessError("The authorised user is not an owner")
                    else:
                        if u_id not in chan['owner']: # user is not the owner
                            raise ValueError("user is not the owner")
                        else:
                            chan['owner'].remove(u_id)
    return dumps({})

@APP.route('/channels/list', methods=['GET'])
def channels_list():
    global user, channel
    token = request.args.get['token']
    for u in user:
        if token == u['token']:
            channels_list == u['channel_list']
    return dumps({
        'channels': channels_list
    })

@APP.route('/channels/listall', methods=['GET'])
def channels_listall():
    global user, channel

    return dumps({
        'channels':channel
    })

@APP.route('/channels/create', methods=['POST'])
def channels_create():
    global channel, user
    token = request.form.get['token']
    name = request.form.get['name']
    is_public = request.form.get['is_public']
    # get information
    if len(name) > 20:
        raise ValueError("Name is more than 20 characters long")
    else:
        channel_id = uuid.uuid1().int
        for u in user:
            if token == u['token']:
                u_id == u['u_id']

        dic = {
            'name': name,
            'channel_id': channel_id,
            'owner': u_id,
            'is_public': is_public
        }
        channel.append(dic)
    return dumps({
        'channel_id': channel_id
    })

@APP.route('/message/sendlater', methods=['POST'])
def message_sendlater():
    global channel, user, message
    token = request.form.get['token']
    channel_id = request.form.get['channel_id']
    message = request.form.get['message']
    time_sent = request.form.get['time_sent']
    # get information
    for chan in channel:
        if channel_id not in chan['channel_id']:# channel exist
            raise ValueError("Channel ID is not a valid channel")
        else:
            message_id = uuid.uuid1().int
            for u in user:
                if token == u['token']:
                    u_id == u['u_id']
                    if channel_id not in u['channel_list']:
                        raise AccessError('The authorised user has not joined the channel')
                else:
                    if len(message) > 1000:
                        raise ValueError('Message is more than 1000 characters')
                    if time_sent < datetime.datetime.now:
                        raise ValueError('Time sent is a time in the past')
                    dic = {
                        'message': message,
                        'message_id': message_id,
                        'user': u_id,
                        'time_sent': time_sent
                    }
                    chan['message'].append(dic)
    return dumps({
        'message_id': message_id
    })

@APP.route('/messsage/send', methods=['POST'])
def message_send():
    global channel, user
    token = request.form.get['token']
    channel_id = request.form.get['channel_id']
    message = request.form.get['message']
    # get information

    for c in channel:
        if channel_id not in c['channel_id']:# channel exist
            raise ValueError("Channel ID is not a valid channel")
        else:
            message_id = uuid.uuid1().int
            for u in user:
                if token == u['token']:
                    u_id == u['u_id']
                    if channel_id not in u['channel_list']:
                        raise AccessError('The authorised user has not joined the channel')
                else:
                    if len(message) > 1000:
                        raise ValueError('Message is more than 1000 characters')
                    else:
                        dic = {
                            'message': message,
                            'message_id': message_id,
                            'user': u_id
                        }
                        c['message'].append(dic)
    return dumps({
        'message_id': message_id
    })
if __name__ == '__main__':
    APP.run(port=(sys.argv[1] if len(sys.argv) > 1 else 5000))
