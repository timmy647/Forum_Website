import pickle

user = [{
    'email':'z5261400@ad.unsw.edu.au',
    'password': 'password',
    'u_id': 0,
    'token': '',
    'name_first': 'name_first',
    'name_last': 'name_last',
    'handle': '',
    'reset_code': 1,
    'login': False,
    'permission_id': 1,
    'reset_code': '',
    'channel_list': [],
    'handle_str': '',
    'profile_img_url': '',
}]
channel = [{
    'name': 'discussion',
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


def reset():
    global user, channel
    with open('userStore.p', 'wb') as FILE:
        pickle.dump(user, FILE)

    with open('channelStore.p', 'wb') as FILE:
        pickle.dump(channel, FILE)

if __name__ == '__main__':
    reset()