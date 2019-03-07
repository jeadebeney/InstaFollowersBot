# Environment variables
from dotenv import load_dotenv
load_dotenv()
# Config
import config
# Defaults
import os
import time
import random
# Pandas
import pandas as pd
# Selenium
from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
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
    print(final_com)
    return final_com

# Create a webdriver instance
def webdriverInstance():
    webdriver = wd.Chrome(executable_path=os.getenv(
    "CHROME_DRIVER_PATH"), options=chrome_options)
    return webdriver



def webdriverConnect(webdriver):
    webdriver.get('https://www.instagram.com/accounts/login/')
    time.sleep(1)
    webdriver.find_element_by_name('username').send_keys(os.getenv("PYI_IG_EMAIL"))
    webdriver.find_element_by_name('password').send_keys(
    os.getenv("PYI_IG_PASSWORD"))
    webdriver.find_element_by_xpath(
    '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[3]/button').send_keys(Keys.ENTER)
    return webdriver


def getTag(webdriver, hashtag_list, tag):
    time.sleep(5)
    webdriver.get('https://www.instagram.com/explore/tags/' + hashtag_list[tag] + '/')
    print("hastag {} envoye".format(hashtag_list[tag]))
    time.sleep(5)


def clickPicture(webdriver):
    first_thumbnail = webdriver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div')
    first_thumbnail.click()
    time.sleep(random.randint(1, 3))

# Creating a hashtag list to scratch instagram
hashtag_list = config.hashtags

# - if it's the first time you run it, use this line and comment the two below
prev_user_list = []

webdriver = webdriverInstance()
webdriver = webdriverConnect(webdriver)

while(1):
    new_followed = []
    tag = -1 
    followed = 0
    likes = 0
    comments = 0
    for hashtag in hashtag_list:

        tag = tag+1


        getTag(webdriver, hashtag_list, tag)

        clickPicture(webdriver)

        try:
            for x in range(1, 200):
                username = webdriver.find_element_by_xpath(
                    '/html/body/div[2]/div[2]/div/article/header/div[2]/div[1]/div[1]/h2/a').text
                print("The username is {}".format(username))

                if username not in prev_user_list:
                    if webdriver.find_element_by_xpath('/html/body/div[2]/div[2]/div/article/header/div[2]/div[1]/div[2]/button').text == 'Follow':
                        if random.randint(1,100) == 53:
                            webdriver.find_element_by_xpath('/html/body/div[2]/div[2]/div/article/header/div[2]/div[1]/div[2]/button').click()
                            new_followed.append(username)
                            followed += 1

                        # Liking the picture
                        button_like = webdriver.find_element_by_xpath(
                            '/html/body/div[2]/div[2]/div/article/div[2]/section[1]/span[1]/button/span')
                        button_like.click()
                        likes += 1

                        time.sleep(random.randint(18, 25))

                        # Comments and tracker
                        print('{}_{}'.format(hashtag, x))
                        comments += 1
                        webdriver.find_element_by_xpath(
                            '/html/body/div[2]/div[2]/div/article/div[2]/section[1]/span[2]/button/span').click()
                        comment_box = webdriver.find_element_by_xpath(
                            '/html/body/div[2]/div[2]/div/article/div[2]/section[3]/div/form/textarea')

                        rand_comment = random_comment()
                        comment_box.send_keys(rand_comment)
                        time.sleep(1)
                        # Enter to post comment
                        comment_box.send_keys(Keys.ENTER)
                        time.sleep(random.randint(22, 28))

                    # Next picture
                    webdriver.find_element_by_link_text('Next').click()
                    time.sleep(random.randint(25, 29))
                else:
                    webdriver.find_element_by_link_text('Next').click()
                    time.sleep(random.randint(20, 26))

        except:
            continue




'''
# To store list of users
# prev_user_list = pd.read_csv('20181203-224633_users_followed_list.csv', delimiter=',').iloc[:,1:2] # useful to build a user log
# prev_user_list = list(prev_user_list['0'])


# TODO: Comment
for n in range(0, len(new_followed)):
    prev_user_list.append(new_followed[n])

updated_user_df = pd.DataFrame(prev_user_list)
updated_user_df.to_csv('{}_users_followed_list.csv'.format(
    time.strftime("%Y%m%d-%H%M%S")))
print('Liked {} photos.'.format(likes))
print('Commented {} photos.'.format(comments))
print('Followed {} new people.'.format(followed))


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


# Wait approximatively the requested amount of time
def random_sleep(seconds):
    time.sleep(seconds + random.randint(10, 1000) / 1000)


'''
