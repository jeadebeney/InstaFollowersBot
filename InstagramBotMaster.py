
import InstagramBotSlave as InstaSlave

import config
# Selenium
from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("disable-infobars")

prev_user_list = []


# Creating a hashtag list to scratch instagram
hashtag_list_1 = config.hashtags_1  
hashtag_list_2 = config.hashtags_2  
hashtag_list_3 = config.hashtags_3  
hashtag_list_4 = config.hashtags_4  




InstaSlave.commentLoop(hashtag_list_1)





