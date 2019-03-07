
import InstagramBotSlave as InstaSlave
from InstagramBotSlave import commentLoop
import config
import threading
import time


prev_user_list = []


# Creating a hashtag list to scratch instagram
hashtag_list_1 = config.hashtags_1  
hashtag_list_2 = config.hashtags_2  
hashtag_list_3 = config.hashtags_3  
hashtag_list_4 = config.hashtags_4  


t1 = threading.Thread(target = commentLoop, args = (hashtag_list_1,))
t2 = threading.Thread(target = commentLoop, args = (hashtag_list_2,))
t3 = threading.Thread(target = commentLoop, args = (hashtag_list_3,))
t4 = threading.Thread(target = commentLoop, args = (hashtag_list_4,))

t1.start()
time.sleep(15)
t2.start()
time.sleep(15)
t3.start()
time.sleep(15)
t4.start()



#t1.join()
#t2.join()





