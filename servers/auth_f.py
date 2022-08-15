from json import dumps
from flask import Flask, request
import jwt
import pickle
from collections import Counter
import re
import uuid
from flask_mail import Mail, Message
import sys
import error


###----------------------------------auth_functions-------------------------------###
user = [{
    'email':'z5261400@ad.unsw.edu.au',
    'password': 'password',
    'u_id': '0',
    'token': '',
    'name_first': 'name_first',
    'name_last': 'name_last',
    'handle': '',
    'reset_code': 1,
    'login': False,
    'permission_id': 1,
    'channel_list': [{
        'channel_id': '',
        'permission': '', # 1 = owner, 2 =member
    },],
}]
channel = [{
    'name': '',
    'channel_id': '',
    'is_public': False,
    'owner': '',
    'member': '',
    'message': [{
        'message': '',
        'message_id': '',
        'user': '',
        'time_sent': '',
        'react_id': [],
        'pin': False,
    }]
}]

def save():
    global user
    with open('userStore.p', 'wb') as FILE:
        pickle.dump(user, FILE)


#check email format
def check_email(email):
    # regular expression
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if re.search(regex, email):
        return True
    else:
        return False


def auth_login(email, password):
    global user
    user = pickle.load(open('userStore.p', 'rb'))

    if not check_email(email):
        # error.invalid_email()
        raise ValueError("Invalid email")
    email_found = 0
    for dic in user:
        if email == dic['email']:
            email_found = 1
            if  password == dic['password']:
                u_id = dic['u_id']
                token = jwt.encode({'u_id': u_id}, 'activate', algorithm='HS256').decode('utf-8')
                dic['login'] = True
                dic['token'] = token
                save()
                return dumps({
                    'u_id': u_id,
                    'token': token,
                })
            else:
                #error.incorrect_password()
                raise ValueError("Incorrect_password")
 
    if email_found == 0:
        #error.unregister_email
        raise ValueError("Unregistered email")


def auth_logout(token):
    global user
    user = pickle.load(open('userStore.p', 'rb'))

    user_found = 0
    for u in user:
        if token == u['token']:
            u['login'] = False
            u_id = u['u_id']
            logout = jwt.encode({'u_id': u_id}, 'logout', algorithm='HS256').decode('utf-8')
            u['token'] = logout
            user_found = 1
    if user_found == 0:
        #error.invalid_token()
        raise ValueError("Invalid token")
        return dumps({
            'is_success': False,
        })

    save()
    return dumps({
        'is_success': True,
    })


def auth_register(email, password, name_first, name_last):
    global user
    user = pickle.load(open('userStore.p', 'rb'))
    if not check_email(email):
        #error.invalid_email()
        raise ValueError("Invalid email")

    # Existing email
    for dic in user:
        if email == dic['email']:
            #error.registered_email()
            raise ValueError("Registered email")

    # Invaild password
    if len(password) < 6:
        #error.input_too_short()
        raise ValueError("Invalid password")

    # name_first is over 50 char
    if len(name_first) > 50:
        #error.input_too_long()
        raise ValueError("First name should not exceed 50 characters")
    # name_last is over 50 char
    if len(name_last) > 50:
        #error.input_too_long()
        raise ValueError("Last name should no t exceed 50 characters")

    u_id = uuid.uuid4().int>>80
    token = jwt.encode({'u_id': u_id}, 'activate', algorithm='HS256').decode('utf-8')
    dic = {
        'email': email,
        'password': password,
        'u_id': u_id,
        'name_first': name_first,
        'name_last': name_last,
        'login': True,
        'permission': 0,
        'token': token,
        'reset_code': 0,
        'channel_list': [],
        'handle_str': '',
        'profile_img_url': '',
        'permission_id': 3,
    }
    user.append(dic)
    save()
    return dumps({
        'u_id': u_id,
        'token': token,
    })

def auth_passwordreset_request(email, mail):
    global user
    user = pickle.load(open('userStore.p', 'rb'))

    # Bad email or Invaild email
    if not check_email(email):
        #error.invalid_email()
        raise ValueError("Invalid email")
    # Unregistered email
    email_found = 0
    for dic in user:
        if email == dic['email']:
            email_found = 1
            reset_code = uuid.uuid1().int
            dic['reset_code'] = reset_code
            save()
    if email_found == 0:
        #error.unregister_email()
        raise ValueError("Unregistered email")

    try:
        msg = Message("Password Reset Request",
                      sender="COMP1531.temporary@gmail.com",
                      recipients=[email])
        msg.body = ("Here is the Passwordreset Code: \n" + str(reset_code))
        mail.send(msg)
        return dumps({})
    except Exception as e:
        return (str(e))


def auth_passwordreset_reset(reset_code, new_password):
    global user
    user = pickle.load(open('userStore.p', 'rb'))

    if len(new_password) < 8:
        raise ValueError("Invaild password")

    # Invalid reset code
    code_found = 0
    for dic in user:
        if reset_code == str(dic['reset_code']) and dic['reset_code'] != 0:
            code_found = 1
            dic['password'] = new_password
            dic['reset_code'] = 0
            save()
            return dumps({})
    # Invalid password
    if code_found == 0:
        #error.invalid_code()
        raise ValueError("Invalide reset code")


def user_profile(token, u_id):
    global user
    user = pickle.load(open('userStore.p', 'rb'))
    
    found = 0
    dic = {}
    for u in user:
        if int(u_id) == u['u_id']:
            found = 1
            dic = {
                'u_id': u['u_id'],
                'email': u['email'],
                'name_first': u['name_first'],
                'name_last': u['name_last'],
                'handle_str': u['handle_str'],
                'profile_img_url': u['profile_img_url'],
            }
    if found == 0:
        raise ValueError("User with u_id is not a valid user")
    print(dic)
    return dumps({
        'user': dic,
    })


def user_profile_setname(token, name_first, name_last):
    global user
    user = pickle.load(open('userStore.p', 'rb'))
    name_first = str(name_first)
    name_last = str(name_last)

    if len(name_first) < 1 or len(name_first) > 50:
        raise ValueError("Name too long")
    if len(name_last) < 1 or len(name_last) > 50:
        raise ValueError("Name too long")
    
    for u in user:
        if str(token) == u['token']:
            u['name_first'] = name_first
            u['name_last'] = name_last
    save()
    return dumps({})

def user_profile_setemail(token, email):
    global user
    user = pickle.load(open('userStore.p', 'rb'))

    email = str(email)

    if not check_email(email):
        # error.invalid_email()
        raise ValueError("Invalid email")

    for dic in user:
        if email == dic['email']:
            #error.registered_email()
            raise ValueError("Registered email")

    for u in user:
        if str(token) == u['token']:
            u['email'] = email
    save()
    return dumps({})

def user_profile_sethandle(token, handle_str):
    global user
    user = pickle.load(open('userStore.p', 'rb'))

    handle_str = str(handle_str)
    if handle_str < 3 or handle_str > 20:
        raise ValueError("Handle_str must be between 3 and 20 characters")

    for u in user:
        if handle_str == u['handle_str']:
            raise ValueError("Handle is already used by another user")

    for u in user:
        if str(token) == u['token']:
            u['handle_str'] = handle_str
    save()
    return dumps({})

def users_all(token):
    global user
    user = pickle.load(open('userStore.p', 'rb'))

    users = []
    for u in user:
        if u['token'] != str(token):
            dic = {
                'u_id': u['u_id'],
                'email': u['email'],
                'name_first': u['name_first'],
                'name_last': u['name_last'],
                'handle_str': u['handle_str'],
                'profile_img_url': u['profile_img_url'],
            }
            users.append(dic)

    return dumps({
        'users': users,
    })


def standup_start(token, channel_id, length):

    return dumps({
        'time_finish': '',
    })

def standup_active(token, channel_id):

    return dumps({
        'is_active': False,
        'time_finish': '',
    })

def standup_send(token, channel_id, message):

    return dumps({})

def search(token, query_str):
    global user, channel
    user = pickle.load(open('userStore.p', 'rb'))
    channel = pickle.load(open('channelStore.p', 'rb'))

    token = str(token)
    query_str = str(query_str)

    messages = []
    for u in user:
        if token == u['token']:
            for ch in u['channel_list']:
                for c in channel:
                    if ch['channel_id'] == c['channel_id']:
                        for mes in c['message']:
                            if query_str == mes['message']:
                                messages.append(mes)

    return dumps({
        'messages': messages,
    })

def admin(token, u_id, permission_id):
    global user, channel
    user = pickle.load(open('userStore.p', 'rb'))

    token = str(token)
    u_id = int(u_id)
    permission_id = int(permission_id)

    auth = 0
    for u in user:
        if token == u['token']:
            if u['permission_id'] == 1:
                auth = 1
            elif u['permission_id'] == 2:
                auth = 2
            else:
                raise AccessError("The authorised user is not an admin or owner")

    if auth == 0:
        raise ValueError("Invaild Token")

    if permission_id > 3 or permission_id < 1:
        raise ValueError("Permission_id does not refer to a value permission")

    if permission_id < auth:
        raise AccessError("The authorised user does not have the permission")

    found = 0
    for u in user:
        if u_id == u['u_id']:
            found = 1
            u['permission_id'] = permission_id

    if found == 0:
        raise ValueError("u_id does not refer to a valid user")

    save()
    return dumps({})