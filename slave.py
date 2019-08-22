# Environment variables
import multiprocessing
import csv
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver as wd
import random
import time
import os
from collections import deque
import logging
import datetime
from tracker import Tracker
import signal
import sys


class Slave(multiprocessing.Process):

    __slots__ = '_driver', '_tracker', '_logger',  '_ig_login', '_ig_password', '_comments', '_hashtags', '_visited_posts', '_followed_users', '_comments_posted', '_liked_posts', '_blocked_count'

    def __init__(self, ig_login, ig_password, comments, hashtags, export_dir):
        super(Slave, self).__init__()
        self._logger = logging.getLogger(f'{ig_login}')
        self._logger.info("__init__")
        self._comments = comments
        # shuffle hashtags to not always start with the same order
        random.shuffle(hashtags)
        self._hashtags = deque(hashtags)
        self._ig_login = ig_login
        self._ig_password = ig_password
        self._tracker = Tracker(f'{export_dir}/{ig_login}.csv')
        self._followed_users = []
        self._comments_posted = []
        self._visited_posts = []
        self._liked_posts = []
        self._blocked_count = 0
        self._driver = None
        # Handle ctrl+C exit signal to print summary
        signal.signal(signal.SIGINT, self._signal_handler)

    def run(self):
        self._reboot()

        while self._hashtags:
            hashtag = self._hashtags.pop()
            self._tracker.track('hashtag', hashtag)
            self._search_hashtag(hashtag)
            self._click_picture()
            time.sleep(3)

            for _ in range(200):
                # reset variables
                username = comment = None
                liked = False
                self._tracker.track('picture', self._driver.current_url)
                self._visited_posts.append(self._driver.current_url)
                username = self._get_current_picture_username()
                try:
                    self._follow_user(username)
                    liked = self._like_picture()
                    if liked:
                        comment = self._comment_picture(username)

                    # Next picture
                    self._next_picture()
                except Exception as e:
                    if self._ig_blocked():
                        self._blocked_count += 1
                        self._tracker.track('blocked')
                        self._reboot()
                        break
                    raise e

    def _init_driver(self):
        ''' Init selenium chrome instance '''
        chrome_options = Options()
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("disable-infobars")
        # selenium logger level
        from selenium.webdriver.remote.remote_connection import LOGGER
        LOGGER.setLevel(logging.WARNING)
        self._driver = wd.Chrome(
            executable_path='./chromedriver', options=chrome_options)
        time.sleep(2)

    def _reboot(self):
        ''' Close and reboot webdriver instance to bypass ig blocking '''

        self._logger.info("rebooting")
        if self._driver:
            self._driver.quit()
            self._driver = None
        self._init_driver()
        self._ig_connect()

    def _random_comment(self):
        ''' Return random comment '''
        return random.choice(self._comments)

    def _follow_user(self, username):
        ''' Follow user sometimes '''
        if random.randint(1, 100) == 1:
            self._logger.info(f"following user {username}")
            self._driver.find_element_by_xpath(
                '/html/body/div[3]/div[2]/div/article/header/div[2]/div[1]/div[2]/button').click()
            self._followed_users.append(username)
            self.random_sleep()
            self._tracker.track('follow', username)
            return True
        return False

    def _ig_connect(self):
        ''' Login to instagram '''
        self._logger.info(f"logging in as {self._ig_login}")
        self._driver.get('https://www.instagram.com/accounts/login/')
        time.sleep(3)
        self._driver.find_element_by_name(
            'username').send_keys(self._ig_login)
        self._driver.find_element_by_name(
            'password').send_keys(self._ig_password)
        time.sleep(0.1)

        login_btn = self._find_element(['//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]/button',
                                        '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[6]/button', ])
        login_btn.send_keys(Keys.ENTER)
        time.sleep(0.5)
        WebDriverWait(self._driver, 10).until(
            lambda x: self._driver.find_element_by_link_text(self._ig_login))

    def _search_hashtag(self, hashtag):
        ''' Search hashtag in ig '''
        self._logger.info(f"searching hashtag: {hashtag}")
        self._driver.get(
            f'https://www.instagram.com/explore/tags/{hashtag}/')
        WebDriverWait(self._driver, 10).until(
            lambda x: x.find_element_by_xpath('//*[@id="react-root"]/section/main/article'))

    def _click_picture(self):
        ''' Click on picture thumbnail '''
        self._logger.info(f"click picture")
        first_thumbnail = self._driver.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div')
        first_thumbnail.click()

    def _get_current_picture_username(self):
        ''' Get current picture owner's username '''
        self._logger.info(f"getting current picture username")
        try:
            username = self._driver.find_element_by_xpath(
                '/html/body/div[3]/div[2]/div/article/header/div[2]/div[1]/div[1]/h2/a').text
        except:
            username = None
        self._logger.info(f"found {username}")
        return username

    def _get_picture_likes(self):
        ''' Get current picutre's number of likes '''
        self._logger.info(f"getting current picture like count")
        try:
            nb_likes = self._driver.find_element_by_xpath(
                '/html/body/div[3]/div[2]/div/article/div[2]/section[2]/div/div/button/span').text
            nb_likes = int(nb_likes.replace(',', ''))
        except Exception:
            # Instagram now hides number of likes for some posts - just return None
            nb_likes = None

        self._logger.info(f"found {nb_likes}")
        return nb_likes

    def _like_picture(self):
        ''' Like picture only if not already liked '''
        # Multiple xpaths exist for the heart like icon - try unitl you find the correct one
        btn_like = self._find_element(['/html/body/div[3]/div[2]/div/article/div[2]/section[1]/span[1]/button/span',
                                       '/html/body/div[2]/div[2]/div/article/div[2]/section[1]/span[1]/button/span',
                                       '/html/body/div[4]/div[2]/div/article/div[2]/section[1]/span[1]/button/span',
                                       ])

        like_classes = btn_like.get_attribute("class")
        if 'filled' not in like_classes:  # look if heart is filled = already liked
            self._logger.info(f"liking current picture - no previous like")
            btn_like.click()
            
            current_post_url = self._driver.current_url
            self._liked_posts.append(current_post_url)
            self._tracker.track('like', current_post_url)
            self.random_sleep()
            return True
        else:
            self._logger.info(f"current picture already liked - skipping")
            return False

    def _comment_picture(self, username):
        ''' Comment picture if available comments '''

        if len(self._comments) == 0:
            return

        self._logger.info(f"commenting current picture")

        comment = self._random_comment()
        # add username to comment
        if random.randint(1, 3) == 1 and username:
            comment = f'@{username} {comment}'
        self._logger.info(f"comment {comment}")
        # focus comment box
        self._driver.find_element_by_xpath(
            '/html/body/div[3]/div[2]/div/article/div[2]/section[1]/span[2]/button/span').click()
        # get comment box and add comment
        comment_box = self._driver.find_element_by_xpath(
            "//textarea[@aria-label='Add a comment…']")
        time.sleep(0.2)
        comment_box.send_keys(comment)
        time.sleep(1)
        # send comment
        comment_box.submit()
        self.random_sleep()
        self._comments_posted.append(comment)
        self._tracker.track('comment', comment)
        return comment

    def _next_picture(self):
        ''' Go to next picutre '''
        self._logger.info(f"next picture")
        self._driver.find_element_by_link_text('Next').click()
        # wait for picture to be loaded
        try:
            WebDriverWait(self._driver, 10).until(
                lambda x: x.find_element_by_xpath("//textarea[@aria-label='Add a comment…']"))
        except:
            self._next_picture()
        # /html/body/div[3]/div[1]/div/div/a[2]

    def random_sleep(self):
        ''' Sleep time modulo randomness '''
        sleep_time = random.randint(6, 12)
        self._logger.info(f"sleeping {sleep_time}s")
        time.sleep(sleep_time)

    def _ig_blocked(self):
        ''' Check if current action is blocked by ig, sleep 10 minutes and try again if it is the case '''
        el = self._driver.find_elements_by_xpath(
            "//*[contains(text(), 'Action Blocked')]")

        if len(el) > 0:
            # blocked by ig
            self._logger.warn(f"BLOCKED BY IG")
            return True
        return False

        # Click on 'Action Blocked' pop-up 'Try again' option
        # self._driver.find_element_by_xpath('/html/body/div[4]/div/div/div[2]/button[2]').click()

    def _find_element(self, xpaths):
        for xp in xpaths:
            try:
                element = self._driver.find_element_by_xpath(xp)
                if element is not None:
                    return element
            except:
                raise Exception("Couldn't find any xpaths from list.")

    def _signal_handler(self, sig, frame):
        ''' Print summary when CTRL+C termination '''
        self._logger.info(f'''{self._ig_login}:
                 \t{len(self._visited_posts)} posts visited
                 \t{len(self._comments_posted)} comments posted
                 \t{len(self._followed_users)} users followed
                 \t{len(self._liked_posts)} posts liked
                 \t{self._blocked_count} ig blocks
                 ''')
        sys.exit(0)
