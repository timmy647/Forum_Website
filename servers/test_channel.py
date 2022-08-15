import pytest
import pickle
import database_reset
from json import dumps
from error import AccessError
from auth_f import auth_register
from channel_f import channel_invite, channel_details, channel_messages, channels_create

###--------------------------test_channel_invite------------------------###

# Invalid channel ID
def test_channel_invite_Invalid_channel_id():
    with pytest.raises(ValueError, match=r"Invalid channel ID"):
        channel_invite("token", 123, 123)
# Invalid user ID
def test_channel_invite_Invalid_user_id():
    with pytest.raises(ValueError, match=r"Invalid user ID"):
        channel_invite("token", 123456789, 111)
def test_channel_invite_not_member():
    auth_register("test1@gmail.com", "password", "tim", "liu")
    auth_register("test2@gmail.com", "password", "tim", "liu")
    user = pickle.load(open('userStore.p', 'rb'))
    for u in user:
        if u["email"] == "test1@gmail.com":
            token1 = u["token"]
        if u["email"] == "test2@gmail.com":
            token2 = u['token']
            u_id2 = u["u_id"]
    channels_create(token2, "channel_2", True)
    channel = pickle.load(open('channelStore.p', 'rb'))
    for c in channel:
        if c['name'] == 'channel_2':
            channel_id = c['channel_id']
    with pytest.raises(ValueError, match=r"The authorised user is not already a member of the channel"):
        channel_invite(channel_id, u_id2, token1)

def test_channel_invite_success():
    user = pickle.load(open('userStore.p', 'rb'))
    for u in user:
        if u["email"] == "test1@gmail.com":
            u_id1 = u["u_id"]
        if u["email"] == "test2@gmail.com":
            token2 = u['token']
    channels_create(token2, "channel_2", True)
    channel = pickle.load(open('channelStore.p', 'rb'))
    for c in channel:
        if c['name'] == 'channel_2':
            channel_id = c['channel_id']
    channel_invite(channel_id, u_id1, token2)

    channel = pickle.load(open('channelStore.p', 'rb'))
    invite_success = 0
    for c in channel:
        if c['name'] == 'channel_2':
            if u_id1 in c['member']:
                invite_success = 1
    assert invite_success == 1


###--------------------------test_channel_details------------------------###
# Invalid channel id
def test_channel_details_Invalid_channel_id():
    with pytest.raises(ValueError, match=r"Invalid channel ID"):
        channel_details("token", 123)

###--------------------------test_channel_messgaes------------------------###
# Invalid channel id
def test_channel_messages_Invalid_channel_id():
    with pytest.raises(ValueError, match=r"Invalid channel ID"):
        channel_messages("token", 123, 321)

def test_channel_messages_check_start():
    with pytest.raises(ValueError, match=r"Start is greater than the toal number of messages"):
        channel_messages("token", 123456789, 1001)


###---------------------------test database_reset---------------------------###
def test_database_reset():
    database_reset.reset()