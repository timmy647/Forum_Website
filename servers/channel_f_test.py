import pytest
from channel_f import*
from channel_f import AccessError

#-----------------------test1---------------------#
def test_channel_leave ():
    auth1 = auth_register("zoe@gmail.com","123456","zoe","li")
    auth2 = auth_register("freya@gmail.com","12345","freya","li")
    # create user imformation

    token1 = auth1["token"]
    token2 = auth2["token"]
    # set user token

    channelsCreate = channels_create(token1,"channelname",True)
    channelId = channelsCreate["channel_id"]
    # set user1 to create public channel
    # get channel Id 

    channel_join(token1,'channelname')
    # set user1 join the channel
    channel_join(token2,'channelname')
    # set user2 join the channel
    channel_leave(token1,'channelname')
    # user1 left channel
    with pytest.raises(ValueError,match=r"channel do not exist"):
         channel_leave(token2,12345)
         # user2 cannot left the channel that do not exist

#-----------------------test2---------------------#
def test_channel_join():
    auth1 = auth_register("zoe@gmail.com","123456","zoe","li")
    auth2 = auth_register("yura@gmail.com","12356","yura","bae")
    auth3 = auth_register("tim@gmail.com","12346","tim","liu")
    # create user imformation

    token1 = auth1["token"]
    token2 = auth2["token"]
    token3 = auth3["token"]
    # set user token

    channelsCreate1 = channels_create(token1,"channelname1",True)
    # user1 create the public channel1 
    channelsCreate2 = channels_create(token1,"channelname2",False)
    # user1 create the private channel2

    channelId1 = channelsCreate["channel_id"]
    channelId2 = channelsCreate["channel_id"]
   
    channel_join(token1,'channelname1')
    # user1 join the channel1(public)
    channel_join(token2,'channelname1')
    # user2 join the channel1(public)
    with pytest.raises(AccessError,match=r"channel do not exist"):
        channel_join(token3,12345)
        # user3 cannot join the channel that not exist

    channel_join(token1,'channelname2')
    # user1 join the channel2(private)   
    with pytest.raises(AccessError,match=r"channel is private"):
        channel_join(token3,'channelname2')
        # user3 cannot join the channel2(private)

#-----------------------test3---------------------#
def test_channel_addowner():
    auth1 = auth_register("zoe@gmail.com","123456","zoe","li")
    auth2 = auth_register("freya@gmail.com","123456","freya","li")
    auth3 = auth_register("yura@gmail.com","123456","yura","bae")
    auth4 = auth_register("tim@gmail.com","123456","tim","liu")
    auth5 = auth_register("john@gmail.com","123456","john","smith")

    token1 = auth1["token"]
    token2 = auth2["token"]
    token3 = auth3["token"]
    token4 = auth4["token"]
    token5 = auth5["token"]

    uid1 = auth1["u_id"]
    uid2 = auth2["u_id"]
    uid3 = auth3["u_id"]
    uid4 = auth4["u_id"]
    uid5 = auth5["u_id"]

    owner_slack = [token2] # assume user2 is the owner of slack
    
    channelsCreate = channels_create(token1,"channelname",True)
    # user1 create channel, set user1 as the owner of the channel 
    channelId = channelsCreate["channel_id"]
    
    channel_join(token1,'channelname')
    channel_join(token2,'channelname')
    channel_join(token3,'channelname')
    channel_join(token4,'channelname')
   
    with pytest.raises(ValueError,match=r"channel do not exist "):
        channel_join(token5,12345)
        # user5 cannot join the channel that not exist

    with pytest.raises(AccessError,match=r"user do not have permission")
        channel_addowner(token3,channelId,uid3)
        # user3 cannnot add user3 as owner
        # since user3 is not the owner of the channel or slack

    channel_addowner(token1,channelId,uid3)
    # user1(the owner of the channel) set the user3 as the owner of the channel
    channel_addowner(token2,channelId,uid4)
    # user2(the owner of the slack) set the user4 as the owner of the channel
    with pytest.raises(ValueError, match=r"user is already the owner of the channel"):
        channel_addowner(token1,channelId,uid1)
        # user1(the owner of the channel) cannnot set itself as the owner
        # since user1 is already the owner
    

#-----------------------test4---------------------#  
def test_channel_removeowner():
    auth1 = auth_register("zoe@gmail.com","123456","zoe","li")
    auth2 = auth_register("yura@gmail.com","123456","yura","bae")
    auth3 = auth_register("Freya@gmail.com","123456","Freya","li")
    auth4 = auth_register("tim@gmail.com","123456","tim","liu")
    # create user imformation

    token1 = auth1["token"]
    token2 = auth2["token"]
    token3 = auth3["token"]
    token4 = auth4["token"]
    # set user token

    uid1 = auth1["u_id"]
    uid2 = auth2["u_id"]
    uid3 = auth3["u_id"]
    uid4 = auth4["u_id"]
    # get u_id of each user

    owner_slack = [token2]
    # set user2 as the owner of the slack

    channelsCreate = channels_create(token1,"channelname",True)
    # user1 create the channel
    # set user1 as the owner of the channel

    channelId = channelsCreate["channel_id"]
    # get channel Id

    channel_join(token1,'channelname')
    channel_join(token2,'channelname')
    channel_join(token3,'channelname')
    channel_join(token4,'channelname')
    
    with pytest.raises(ValueError,match=r"channel do not exist "):
        channel_join(token4,12345)
        # user4 cannot join the channel that not exist

    with pytest.raises(AccessError,match=r"user do not have permission")
        channel_removeowner(token3,channelId,uid1)
        # user3 cannnot remove user1(owner of the channel)
        # since user3 is not the owner of the channel or slack
    with pytest.raises(ValueError, match=r"user is not the owner of the channel"):
        channel_removeowner(token1,channelId,uid3)
        # user1(the owner of the channel) cannnot remove user3
        # since user3 is not the owner

    channel_removeowner(token1,channelId,uid1)
    # user1(the owner of the channel) remove user1 

#-----------------------test5---------------------# 
def test_channels_list():
    pass
    
#-----------------------test6---------------------# 
def test_channels_listall():
    pass

#-----------------------test7---------------------# 
def channels_create():
    auth1 = auth_register("zoe@gmail.com","123456","zoe","li")
    auth2 = auth_register("Freya@gmail.com","12346","Freya","li")
    # create user information

    token1 = auth1["token"]
    token2 = auth2["token"]

    channelsCreate = channels_create(token1,"channelname",True)
    # user1 create the channel
    channelId = channelsCreate["channel_id"]
    # set channel id
    with pytest.raises(ValueError,match=r"channel name is more than 20 characters"):
        channels_create(token2,"a"*22,True)
        # user2 use the channel name  that more than 20 character

