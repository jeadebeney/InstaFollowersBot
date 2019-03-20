# Environment variables
from dotenv import load_dotenv
load_dotenv()
import config
import os
import time
import random
import numpy as np
from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import csv
chrome_options = Options()
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("disable-infobars")





# Return a random comment from config file
def random_comment():
    com_1 = random.choice(config.comments_adjectif)
    com_2 = random.choice(config.comments_photo)
    com_3 = random.choice(config.comments_smiley)
    com_4 = random.choice(config.comments_ponctuation)
    final_com = com_1 + " " + com_2 + " " + com_3+ com_4
    return [final_com, com_1, com_2, com_3]


# Create a webdriver instance
def webdriverInstance():
    webdriver = wd.Chrome(executable_path=os.getenv(
    "CHROME_DRIVER_PATH"), options=chrome_options)
    time.sleep(2)
    return webdriver


def webdriverConnect(webdriver):
    webdriver.get('https://www.instagram.com/accounts/login/')
    time.sleep(3)
    webdriver.find_element_by_name('username').send_keys(os.getenv("PYI_IG_EMAIL"))
    webdriver.find_element_by_name('password').send_keys(
    os.getenv("PYI_IG_PASSWORD"))
    webdriver.find_element_by_xpath(
    '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[3]/button').send_keys(Keys.ENTER)


def getTag(webdriver, hashtag_list, tag):
    time.sleep(5)
    webdriver.get('https://www.instagram.com/explore/tags/' + hashtag_list[tag] + '/')
    #print("hastag {} envoye".format(hashtag_list[tag]))
    time.sleep(5)


def clickPicture(webdriver):
    first_thumbnail = webdriver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div')
    first_thumbnail.click()
    time.sleep(random.randint(1, 3))


# get Username when the browser displays a picture (full screen)
def getUsername(webdriver):
    username = webdriver.find_element_by_xpath('/html/body/div[2]/div[2]/div/article/header/div[2]/div[1]/div[1]/h2/a').text
    #print("The username is {}".format(username))
    return username


# get number of likes in the current picture we are looking at
def getNumberLikes(webdriver):
    numberLikes =  webdriver.find_element_by_xpath('/html/body/div[2]/div[2]/div/article/div[2]/section[2]/div/div/button/span').text   
    return numberLikes


# get the time picture was posted
def getTime(webdriver):
    timePosted = webdriver.find_element_by_xpath('/html/body/div[2]/div[2]/div/article/div[2]/div[2]/a/time'.text)
    return timePosted


# new_followed is a list which tracks previous followed users and followed counts them
def followUser(webdriver, username, new_followed, followed):
    webdriver.find_element_by_xpath('/html/body/div[2]/div[2]/div/article/header/div[2]/div[1]/div[2]/button').click()
    new_followed.append(username)
    followed += 1


# likes count the number of likes given
def likePicture(webdriver, likes):
    time.sleep(random.randint(1,3))
    button_like = webdriver.find_element_by_xpath('/html/body/div[2]/div[2]/div/article/div[2]/section[1]/span[1]/button/span')
    button_like.click()
    likes += 1
    time.sleep(random.randint(11, 25))
    return likes


def commentPicture(webdriver, comments):
    webdriver.find_element_by_xpath(
        '/html/body/div[2]/div[2]/div/article/div[2]/section[1]/span[2]/button/span').click()
    comment_box = webdriver.find_element_by_xpath(
        '/html/body/div[2]/div[2]/div/article/div[2]/section[3]/div/form/textarea')
    rand_comment_list = random_comment()
    rand_comment = rand_comment_list[0]
    comment_box.send_keys(rand_comment)
    time.sleep(1)
    comments += 1
    comment_box.send_keys(Keys.ENTER)
    time.sleep(random.randint(18, 28))
    return rand_comment_list,  comments


def nextPicture(webdriver):
    webdriver.find_element_by_link_text('Next').click()
    time.sleep(random.randint(25, 29))


def commentLoop(hashtag_list, export_path):
    webdriver = webdriverInstance()
    webdriverConnect(webdriver)
    new_followed = []
    tag = -1 
    followed = 0
    likes = 0
    num_comment = 0

    # create a csv file if does not exist yet
    if os.path.isfile(export_path) == False:
        tracking_header = ['ID_user', 'Nb_likes', 'Hashtag', 'Com_part_1', 'Com_part_2', 'Com_part_3']
        with open(export_path, mode = 'w') as header:
            header_writer = csv.writer(header, delimiter = ',')
            header_writer.writerow(tracking_header)


    #tracking_tab = np.array(['ID_user', 'Nb_likes', 'Hashtag', 'Com_part_1', 'Com_part_2', 'Com_part_3'])
    while(1):
        for hashtag in hashtag_list:
            tag = tag+1
            getTag(webdriver, hashtag_list, tag)
            clickPicture(webdriver)
            try:
                for x in range(1, 200):
                    username = getUsername(webdriver)

                    if webdriver.find_element_by_xpath('/html/body/div[2]/div[2]/div/article/header/div[2]/div[1]/div[2]/button').text == 'Follow':
                        
                        # We randomly follow users (odds: 1/100 so far)
                        if random.randint(1,100) == 53:
                            followUser(webdriver, username, new_followed, followed)

                        # Liking the picture
                        likes = likePicture(webdriver, likes)

                        # Comments and tracker
                        comment, num_comment = commentPicture(webdriver, num_comment)
                        
                        # Keeping track of the user info
                        likes_picture = getNumberLikes(webdriver)
                        com_1 = comment[1]
                        com_2 = comment[2]
                        com_3 = comment[3]
                        info_picture = [username,likes_picture,hashtag,com_1,com_2,com_3]

                        with open(export_path, mode = 'a') as tracking_file:
                            track_writer = csv.writer(tracking_file, delimiter = ',')
                            track_writer.writerow(info_picture)

                    if likes % 50 == 0:
                        print("The number of likes is: {}.".format(likes))
                    if num_comment % 50 == 0:
                        print("The number of comments is: {}.".format(num_comment))

                    # Next picture
                    nextPicture(webdriver)

            except:
                continue
                    


'''
# TODO: snake case in python
def unfollow_with_username(self, username):
    self.browser.get('https://www.instagram.com/' + username + '/')
    time.sleep(2)
    follow_btn = self.browser.find_element_by_css_selector('button')
    if (follow_btn.text == 'Following'):
        follow_btn.click()
        time.sleep(2)
        confirmButton = self.browser.find_element_by_xpath(
            '//button[text() = "Unfollow"]')
        confirmButton.click()
    else:
        print("You are not following this user")
'''

