# Environment variables
import threading
import csv
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium import webdriver as wd
import random
import time
import os
from collections import deque
from config import CHROME_DRIVER_PATH
import traceback
import logging


class Slave(threading.Thread):

    def __init__(self, ig_login, ig_password, comments, hashtags, export_dir):
        super(Slave, self).__init__()
        self._logger = logging.getLogger(f'{__name__}-{ig_login}')
        self._logger.debug("__init__")
        self._comments = comments
        self._hashtags = deque(hashtags)
        self._ig_login = ig_login
        self._ig_password = ig_password
        self._export_path = f'{export_dir}/{ig_login}.csv'
        self._new_followed = []
        self._num_comments = 0
        self._likes = 0

        self._init_webdriver()
        self._ig_connect()
        self._init_export(export_dir)
        # launch thread
        self.start()

    def _follow_user(self, username):
        ''' Follow user sometimes '''
        if random.randint(1, 100) == 1:
            self._logger.debug(f"following user {username}")
            self._webdriver.find_element_by_xpath(
                '/html/body/div[3]/div[2]/div/article/header/div[2]/div[1]/div[2]/button').click()
            self._new_followed.append(username)

    def run(self):
        while self._hashtags:
            hashtag = self._hashtags.popleft()
            self._logger.debug(f"current hashtag: {hashtag}")
            self.random_sleep()
            self._search_hashtag(hashtag)
            self.random_sleep()
            self._click_picture()
            self.random_sleep()
            try:
                for _ in range(200):
                    username = self._get_current_picture_username()
                    self._follow_user(username)
                    self.random_sleep()
                    self._like_picture()
                    self.random_sleep()
                    self._comment_picture(username)
                    tracking_data = [hashtag, username,
                                     self._get_picture_likes()]
                    self._update_export_file(tracking_data)

                    # Next picture
                    self._next_picture()
                    self.random_sleep()

            except Exception:
                print("Something went wrong.")
                print(traceback.print_exc())
                continue

    def _update_export_file(self, data):
        ''' Append new row to export file '''
        self._logger.debug(f"update export file: {data}")
        with open(self._export_path, mode='a') as tracking_file:
            track_writer = csv.writer(tracking_file, delimiter=',')
            track_writer.writerow(data)

    def _random_comment(self):
        ''' Return random comment '''
        return random.choice(self._comments)

    # Create a webdriver instance

    def _init_webdriver(self):
        ''' Init selenium chrome instance '''
        chrome_options = Options()
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("disable-infobars")

        from selenium.webdriver.remote.remote_connection import LOGGER
        LOGGER.setLevel(logging.WARNING)
        self._webdriver = wd.Chrome(
            executable_path=CHROME_DRIVER_PATH, options=chrome_options)
        self.random_sleep()

    def _ig_connect(self):
        ''' Login to instagram '''
        self._webdriver.get('https://www.instagram.com/accounts/login/')
        self.random_sleep()
        self._webdriver.find_element_by_name(
            'username').send_keys(self._ig_login)
        self._webdriver.find_element_by_name(
            'password').send_keys(self._ig_password)
        self._webdriver.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]/button').send_keys(Keys.ENTER)

    def _init_export(self, export_dir):
        ''' Init export dir and file if needed '''
        # Create required directories
        if not os.path.exists(export_dir):
            os.makedirs(export_dir)
        # create a csv file if does not exist yet
        if os.path.isfile(self._export_path) == False:
            tracking_header = ['hashtag', 'username', 'nb_likes']
            with open(self._export_path, mode='w') as header:
                header_writer = csv.writer(header, delimiter=',')
                header_writer.writerow(tracking_header)

    def _search_hashtag(self, hashtag):
        ''' Search hashtag in ig '''
        self._logger.debug(f"searching hashtag {hashtag}")
        self._webdriver.get(
            f'https://www.instagram.com/explore/tags/{hashtag}/')

    def _click_picture(self):
        ''' Click on picture thumbnail '''
        self._logger.debug(f"click picture")
        first_thumbnail = self._webdriver.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div')
        first_thumbnail.click()

    def _get_current_picture_username(self):
        ''' Get current picture owner's username '''
        self._logger.debug(f"getting current picture username")
        try:
            username = self._webdriver.find_element_by_xpath(
                '/html/body/div[3]/div[2]/div/article/header/div[2]/div[1]/div[1]/h2/a').text
        except:
            username = None
        self._logger.debug(f"found {username}")
        return username

    def _get_picture_likes(self):
        ''' Get current picutre's number of likes '''
        self._logger.debug(f"getting current picture like count")
        nb_likes = self._webdriver.find_element_by_xpath(
            '/html/body/div[3]/div[2]/div/article/div[2]/section[2]/div/div/button/span').text
        self._logger.debug(f"found {nb_likes}")
        return nb_likes

    def _like_picture(self):
        ''' Like picture '''
        self._logger.debug(f"liking current picture")
        button_like = self._webdriver.find_element_by_xpath(
            '/html/body/div[3]/div[2]/div/article/div[2]/section[1]/span[1]/button/span')
        button_like.click()
        self._likes += 1

    def _comment_picture(self, username):
        ''' Comment picture '''
        self._logger.debug(f"commenting current picture")
        self._num_comments += 1
        self._webdriver.find_element_by_xpath(
            '/html/body/div[3]/div[2]/div/article/div[2]/section[1]/span[2]/button/span').click()
        comment = self._random_comment()

        # add username to comment
        if random.randint(1, 3) == 1 and username:
            comment = f'@{username} {comment}'
        self._logger.debug(f"comment {comment}")
        # get comment box
        comment_box = self._webdriver.find_element_by_xpath(
            '/html/body/div[3]/div[2]/div/article/div[2]/section[3]/div/form/textarea')
        comment_box.send_keys(comment)
        self.random_sleep()
        # send comment
        comment_box.send_keys(Keys.ENTER)
        self.random_sleep()

    def _next_picture(self):
        ''' Go to next picutre '''
        self._logger.debug(f"next picutre")
        self._webdriver.find_element_by_link_text('Next').click()

    def random_sleep(self):
        time.sleep(random.randint(3, 6))
