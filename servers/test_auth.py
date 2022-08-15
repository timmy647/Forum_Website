import pytest
from error import AccessError
from auth_f import auth_login, auth_logout, auth_register, auth_passwordreset_request, auth_passwordreset_reset
from json import dumps
import jwt
import pickle
import os
import database_reset
import sys
from flask_cors import CORS
from flask_mail import Mail, Message
from flask import Flask, request

APP = Flask(__name__)
APP.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='COMP1531.temporary@gmail.com',
    MAIL_PASSWORD="M13A-FZY"
)
CORS(APP)
mail = Mail(APP)

###-------------------------------test auth_login-------------------------------###
# Invaild email test
def test_auth_login_Invaild_email():
    with pytest.raises(ValueError, match=r'Invaild email'):
        auth_login('not_an_email_format', 'password')
# Unregistered email test
def test_auth_login_Unregistered_email():
    with pytest.raises(ValueError, match=r'Unregistered email'):
        auth_login('not_exist@email.com', 'password')
# Incorrect password test
def test_auth_login_Incorrect_password():
    with pytest.raises(ValueError, match=r'Incorrect password'):
        auth_login('z5261400@ad.unsw.edu.au', 'incorrect_password')
# Login in successfully
def test_auth_login_Success():
    user = pickle.load(open('userStore.p', 'rb'))
    for u in user:
        if u['email'] == 'z5261400@ad.unsw.edu.au':
            email = u['email']
            password = u['password']
            name_first = u['name_first']
            name_last = u['name_last']
            u_id = u['u_id']
    token = jwt.encode({'u_id': u_id}, 'activate', algorithm='HS256').decode('utf-8')
    assert auth_login('z5261400@ad.unsw.edu.au', 'password') == dumps({
        'u_id': u_id,
        'token': token,
    })

###-------------------------------test auth_logout-------------------------------###
def test_auth_logout_Invalid_token():
    token = 'Invalid token'
    with pytest.raises(ValueError, match=r'Invalid token'):
        auth_logout(token)
def test_auth_logout_success():
    # already login in test_auth_login_success
    user = pickle.load(open('userStore.p', 'rb'))
    for u in user:
        if u['email'] == 'z5261400@ad.unsw.edu.au':
            token = u['token']

    auth_logout(token)
    user = pickle.load(open('userStore.p', 'rb'))
    for u in user:
        if u['email'] == 'z5261400@ad.unsw.edu.au':
            assert u['login'] == False




###-------------------------------test auth_register-------------------------------###
# Invaild email
def test_auth_register_Invaild_email():
    with pytest.raises(ValueError, match=r'Invalid email'):
        auth_register('not_an_email_format', 'password', 'name_first', 'name_last')
# Registered email
def test_auth_register_registered_email():
    user = pickle.load(open('userStore.p', 'rb'))
    with pytest.raises(ValueError, match=r'Registered email'):
        auth_register('z5261400@ad.unsw.edu.au', 'password', 'name_first', 'name_last')
        auth_register('z5261400@ad.unsw.edu.au', 'password', 'name_first', 'name_last')
# Invaild password
def test_auth_register_Invalid_password():
    with pytest.raises(ValueError, match=r'Invalid password'):
        auth_register('exist@email.com', '123', 'name_first', 'name_last')
# name_first is over 50 char
def test_auth_register_first_name_overflow():
    with pytest.raises(ValueError, match=r'First name should not exceed 50 characters'):
        auth_register('exist@email.com', 'password', 
        '....................51.characters..................', 'name_last')
# name_last is over 50 char
def test_auth_register_last_name_overflow():
    with pytest.raises(ValueError, match=r'Last name should not exceed 50 characters'):
        auth_register('exist@email.com', 'password', 'name_first',
        '....................51.characters..................')
# register success
def test_auth_register_success():
    user = pickle.load(open('userStore.p', 'rb'))
    auth_register('hello@email.com', 'password', 'name_first', 'name_last')
    found = 0
    for u in user:
        if u['email'] == 'hello@email.com':
            found = 1
            assert found == 1

###---------------------------test auth_passwordreset_request---------------------------###
# Invaild email test
def test_auth_passwordreset_request_Invaild_email():
    global mail
    with pytest.raises(ValueError, match=r'Invaild email'):
        auth_passwordreset_request('not_an_email_format', mail)
# Unregistered email test
def test_auth_passwordreset_request_Unregistered_email():
    global mail
    with pytest.raises(ValueError, match=r'Unregistered email'):
        auth_passwordreset_request('not_exist@email.com', mail)
# success
def test_auth_passwordreset_request_Success():
    global mail
    auth_register('tim@email.com', 'password', 'name_first', 'name_last')
    auth_passwordreset_request('tim@email.com', mail)
    pass

###---------------------------test auth_passwordreset_reset---------------------------###
# Invalid reset code
def test_auth_passwordreset_reset_Invalid_reset_code():
    with pytest.raises(ValueError, match=r'Invalide reset code'):
        auth_passwordreset_reset('Invalid reset code', 'password')
# Invalid password
def test_auth_passwordreset_reset_Invalid_password():
    with pytest.raises(ValueError, match=r'Invalid password'):
        auth_passwordreset_reset('Reset code', '123')


###---------------------------test database_reset---------------------------###
def test_database_reset():
    database_reset.reset()
