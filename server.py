"""Flask server"""
import sys
from flask_cors import CORS
from json import dumps
from flask import Flask, request
from servers import auth_f
from servers import channel_f
from flask_mail import Mail, Message
from servers import f_part2

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

@APP.route('/echo/get', methods=['GET'])
def echo1():
    """ Description of function """
    return dumps({
        'echo' : request.args.get('echo'),
    })

@APP.route('/echo/post', methods=['POST'])
def echo2():
    """ Description of function """
    return dumps({
        'echo' : request.form.get('echo'),
    })

@APP.route('/auth/register', methods=['POST'])
def register():
    email = request.form.get('email')
    password = request.form.get('password')
    name_first = request.form.get('name_first')
    name_last = request.form.get('name_last')
    return auth_f.auth_register(email, password, name_first, name_last)

@APP.route('/auth/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    return auth_f.auth_login(email, password)

@APP.route('/auth/logout', methods=['POST'])
def logout():
    token = request.form.get('token')
    return auth_f.auth_logout(token)

@APP.route('/auth/passwordreset/request', methods=['POST'])
def passwordreset_request():
    email = request.form.get('email')
    global mail
    return auth_f.auth_passwordreset_request(email, mail)

@APP.route('/auth/passwordreset/reset', methods=['POST'])
def passwordreset_reset():
    reset_code = request.form.get('reset_code')
    new_password = request.form.get('new_password')
    return auth_f.auth_passwordreset_reset(reset_code, new_password)

@APP.route('/channel/invite', methods=['POST'])
def channel_invite():
    channel_id = request.form.get('channel_id')
    u_id = request.form.get('u_id')
    token = request.form.get('token')
    return channel_f.channel_invite(channel_id, u_id, token)

@APP.route('/channel/details', methods=['GET'])
def channel_details():
    channel_id = request.args.get('channel_id')
    token = request.args.get('token')
    return channel_f.channel_details(channel_id, token)

@APP.route('/channel/messages', methods=['GET'])
def channel_messages():
    channel_id = request.args.get('channel_id')
    start = request.args.get('start')
    token = request.args.get('token')
    return channel_f.channel_messages(token, channel_id, start)

@APP.route('/channel/leave', methods=['POST'])
def channel_leave():
    channel_id = request.form.get('channel_id')
    token = request.form.get('token')
    return channel_f.channel_leave(token, channel_id)

@APP.route('/channel/join', methods=['POST'])
def channel_join():
    channel_id = request.form.get('channel_id')
    token = request.form.get('token')
    return channel_f.channel_join(token, channel_id)

@APP.route('/channel/addowner', methods=['POST'])
def channel_addowner():
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    u_id = request.form.get('u_id')
    return channel_f.channel_addowner(token, channel_id, u_id)

@APP.route('/channel/removeowner', methods=['POST'])
def channel_removeowner():
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    u_id = request.form.get('u_id')
    return channel_f.channel_removeowner(token, channel_id, u_id)

@APP.route('/channels/list', methods=['GET'])
def channels_list():
    token = request.args.get('token')
    return channel_f.channels_list(token)

@APP.route('/channels/listall', methods=['GET'])
def channels_listall():
    token = request.args.get('token')
    return channel_f.channels_listall(token)

@APP.route('/channels/create', methods=['POST'])
def channels_create():
    token = request.form.get('token')
    name = request.form.get('name')
    is_public = request.form.get('public')
    return channel_f.channels_create(token, name, is_public)

@APP.route('/message/send', methods=['POST'])
def message_send():
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    message = request.form.get('message')
    return channel_f.message_send(token, channel_id, message)

@APP.route('/user/profile', methods=['GET'])
def user_profile():
    token = request.args.get('token')
    u_id = request.args.get('u_id')
    return auth_f.user_profile(token, u_id)

@APP.route('/user/profile/setname', methods=['PUT'])
def user_profile_setname():
    token = request.form.get('token')
    name_first = request.form.get('name_first')
    name_last = request.form.get('name_last')
    return auth_f.user_profile_setname(token, name_first, name_last)

@APP.route('/user/profile/setemail', methods=['PUT'])
def user_profile_setemail():
    token = request.form.get('token')
    email = request.form.get('email')
    return auth_f.user_profile_setemail(token, email)

@APP.route('/user/profile/sethandle', methods=['PUT'])
def user_profile_sethandle():
    token = request.form.get('token')
    handle_str = request.form.get('handle_str')
    return auth_f.user_profile_sethandle(token, handle_str)

@APP.route('/users/all', methods=['GET'])
def users_all():
    token = request.args.get('token')
    return auth_f.users_all(token)

@APP.route('/standup/start', methods=['POST'])
def standup_start():
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    length = request.form.get('length')
    return auth_f.standup_start(token, channel_id, length)

@APP.route('/standup/active', methods=['GET'])
def standup_active():
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    return auth_f.standup_active(token, channel_id)

@APP.route('/standup/send', methods=['POST'])
def standup_send():
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    message = request.form.get('message')
    return auth_f.standup_send(token, channel_id, message)


@APP.route('/search', methods=['GET'])
def search():
    token = request.args.get('token')
    query_str = request.args.get('query_str')
    return auth_f.search(token, query_str)

@APP.route('/admin/userpermission/change', methods=['POST'])
def admin():
    token = request.form.get('token')
    u_id = request.form.get('u_id')
    permission_id = request.form.get('permission_id')
    return auth_f.admin(token, u_id, permission_id)


if __name__ == '__main__':
    APP.run(port=(sys.argv[1] if len(sys.argv) > 1 else 5012))
