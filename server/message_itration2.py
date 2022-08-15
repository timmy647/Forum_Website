import sys
from json import dumps
from flask import Flask, request, jsonify
from Error import AccessError

APP = Flask(__name__)

user = [{
    'email':'',
    'password': '',
    'u_id': '',
    'token': '',
    'first name': '',
    'last name': '',
    'reset_code': '',
    'login': False,
    'permission_id': 1,
    'channel_list': [{
        'channel_id': '',
        'permission': ''
    }]
}]


channel = [{
    'name':'',
    'channel':'',
    'channel_id':'',
    'is_public': False,
    'channel_listall':[],
    'owner':[],
    'message': [{
        'message' :'',
        'message_id':'',
        'user':'',
        'time_sent':'',
        'react_id': 0,
        'pin': False
    }]
}]


@APP.route('/message/remove', methods=['DELETE'])
def message_remove():
    global user, channel
    message_id = request.form.get['message_id']
    token = request.form.get('token')

    for u in user:
        if token == u['token']:
            authorised = u['u_id']
            permission_of_auth = u['permission_id']

    have_message = false

    for c in channel:
        for m in c['message']:
            if message_id == m['message_id']:
                have_message = True
                if message['user'] == authorised:
                    c['message'].remove('m')
                else:
                    if permission_of_auth != 3:
                        c['message'].remove('m')
                    elif user not in c['owner']:
                        c['message'].remove('m')
                    else:
                        AssessError('Not sent by the authorised user and No permission')
            else:
                continue

    if have_message == False:
        raise ValueError('Message does not exists')

    return dumps({})



@APP.route('/message/edit', methods=['PUT'])
def message_edit():
    global user, channel
    message_id = request.form.get['message_id']
    token = request.form.get['token']
    edited_message = request.form.get['message']

    for u in user:
        if token == u['token']:
            authorised = u['u_id']
            permission_of_auth = u['permission_id']

    have_message = false

    for c in channel:
        for m in c['message']:
            if message_id == m['message_id']:
                have_message = True
                if message['user'] == authorised:
                    m['message'] = edited_message
                else:
                    if permission_of_auth != 3:
                        m['message'] = edited_message
                    elif user not in c['owner']:
                        m['message'] = edited_message
                    else:
                        AssessError('Not sent by the authorised user and No permission')
            else:
                continue

    if have_message == False:
        raise ValueError('Message does not exists')

    return dumps({})


@APP.route('/message/react', methods=['POST'])
def message_react():
    global user, channel
    message_id = request.form.get['message_id']
    token = request.form.get['token']
    react_id = request.form.get['react_id']
    if react_id != 1:
        raise ValueError('Not a valid react_id')

    for u in user:
        if token == u['token']:
            channel_list = u['channel_list']

    have_message = false
    for c in channel:
        for m in c['message']:
            if message_id == m['message_id']:
                if c not in channel_list:
                    raise ValueError('Have not join the channel where message is')
                elif m['react_id'] == 1:
                    raise ValueError('The message has already been reacted')
                else:
                    m['react_id'] = 1
            else:
                continue

    return dumps({})


@APP.route('/message/unreact', methods=['POST'])
def message_unreact():
    global user, channel
    message_id = request.form.get['message_id']
    token = request.form.get['token']
    react_id = request.form.get['react_id']
    if react_id != 1:
        raise ValueError('Not a valid react_id')

    for u in user:
        if token == u['token']:
            channel_list = u['channel_list']

    have_message = false
    for c in channel:
        for m in c['message']:
            if message_id == m['message_id']:
                if c not in channel_list:
                    raise ValueError('Have not join the channel where message is')
                elif m['react_id'] != 1:
                    raise ValueError('The message has not been reacted')
                else:
                    m['react_id'] = 0
            else:
                continue


    return dumps({})

@APP.route('/message/pin', methods=['POST'])
def message_pin():
    global user, channel
    message_id = request.form.get['message_id']
    token = request.form.get['token']

    for u in user:
        if token == u['token']:
            authorised = u['u_id']
            if u['permission_id'] == 3:
                raise ValueError('No permission')

    have_message = false
    for c in channel:
        for m in c['message']:
            if message_id == m['message_id']:
                if c not in channel_list:
                    raise AccessError('Have not join the channel where message is')
                elif m['pin'] != True:
                    raise ValueError('The message has already been pinned')
                else:
                    m['pin'] = False
            else:
                continue

    if have_message == False:
        raise ValueError('Message_id is not valid')


@APP.route('/message/unpin', methods=['POST'])
def message_unpin():
    global user, channel
    message_id = request.form.get['message_id']
    token = request.form.get['token']

    for u in user:
        if token == u['token']:
            authorised = u['u_id']
            if u['permission_id'] == 3:
                raise ValueError('No permission')

    have_message = false
    for c in channel:
        for m in c['message']:
            if message_id == m['message_id']:
                if c not in channel_list:
                    raise AccessError('Have not join the channel where message is')
                elif m['pin'] != False:
                    raise ValueError('The message have not been pinned')
                else:
                    m['pin'] = True
            else:
                continue

    if have_message == False:
        raise ValueError('Message_id is not valid')


@APP.route('user/profile', methods=['GET'])
def user_profile():
    global user
    token = request.form.get['token']
    u_id = token = request.form.get['u_id']

    has_user = False
    for u in user:
        if u_id == u['u_id'] and token == u['token']:
            curr_email = u['email']
            curr_namefirst = u['namefirst']
            curr_namelast = u['namelast']
            curr_handle = u['handle']

    return dumps({
        'email': curr_email,
        'name_first': curr_namefirst,
        'name_last':curr_namelast,
        'handle_str': curr_handle
    })



if __name__ == '__main__':
    APP.run(port=(sys.argv[1] if len(sys.argv) > 1 else 5000))
