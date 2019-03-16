
import InstagramBotSlave as InstaSlave
from InstagramBotSlave import commentLoop
import config
import threading
import time


prev_user_list = []


# Creating 4 threads instances

t1 = threading.Thread(target = commentLoop, args = (config.hashtags_5,config.export_path_1,))
t2 = threading.Thread(target = commentLoop, args = (config.hashtags_6,config.export_path_2,))
t3 = threading.Thread(target = commentLoop, args = (config.hashtags_7,config.export_path_3,))
t4 = threading.Thread(target = commentLoop, args = (config.hashtags_8,config.export_path_4,))


# Launching 4 different threads
t1.start()
time.sleep(15)
t2.start()
time.sleep(15)
t3.start()
time.sleep(15)
t4.start()






