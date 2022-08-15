import pytest
from message_f import*
from message_f import AccessError

#-----------------------test8---------------------#    
def test_message_sendlater():
        auth1 = auth_register("zoe@gmail.com","123456","zoe","li")
        auth2 = auth_register("yura@gmail.com","123456","yura","bae")
        auth3 = auth_register("Freya@gmail.com","123456","Freya","li")

        token1 = auth1["token"]
        token2 = auth2["token"]
        token3 = auth3["token"]

        channelsCreate = channels_create(token1,"channelname",True)
        # user1 create the public channel
        channelId = channelsCreate["channel_id"]
        # set channel id

        channel_join(token1,'channelname')
        channel_join(token2,'channelname')

        time_sent1 = datetime(2020,10,1,12,20)
        # set time1 in future
        time_sent2 = datetime(2008,10,1,12,20)
        # set time2 in past

        with pytest.raises(ValueError,match=r"channel do not exist"):  
            channel_join(token3,12345)
            # user3 cannot join the channel that not exist 

        with pytest.raises(ValueError,match=r"Message is more than 1000 characters"):
            message_send(token2,channelID,"a"*1002,time_sent1)
            # user2 sent message that more than 1000 characters
        
        message_send(token1,channelId,"Hello",time_sent1)
        # user1 sent message in the future    
        with pytest.raises(ValueError,match=r"Time sent is a time in the past")
            message_send(token2,channelID,"Hello",time_sent2)
            # user2 cannnot sent message in the past

#-----------------------test9---------------------# 
def test_message_send():
        auth1 = auth_register("zoe@gmail.com","123456","zoe","li")
        auth2 = auth_register("yura@gmail.com","123456","yura","bae")
        auth3 = auth_register("Freya@gamil.com","123","Freya","li")

        token1 = auth1["token"]
        token2 = auth2["token"]
        token3 = auth3["token"]

        channelsCreate = channels_create(token1,"channelname",True)
        # user1 create the channel
        channelId = channelsCreate["channel_id"]

        channel_join(token1,'channelname')
        # user1 join channel
        channel_join(token2,'channelname')
        # user2 join channel

        with pytest.raises(ValueError,match=r"channel do not exist"):  
            channel_join(token3,12345)
            # use3r cannot join the channel that not exist 
        
        message_send(token1,channelId,"Hello")
        # user1 sent message in channel
        with pytest.raises(ValueError,match=r"Message is more than 1000 characters"):
            message_send(token2,channelID,"a"*1002)
            # user2 sent message that more than 1000 character in channel 
