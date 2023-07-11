from typing import List, Any, Union
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
import os
import time
from urllib import request
import urllib


class IGbot:

    last_height: Union[Union[int, List[Union[int, str]]], Any]
    new_height: Union[Union[int, List[Union[int, str]]], Any]

    def __init__(self, username, password):

        self.username = username
        self.password = password
        self.driver = webdriver.Chrome('chromedriver.exe')
        self.base_url = 'https://www.instagram.com/'
        self.ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)
        self.login()

    def login(self):

        self.driver.get(self.base_url + 'accounts/login/')
        self.driver.implicitly_wait(3)

        # fill username field
        self.write_text('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[2]/div/label/input',
                        self.username)

        # fill password field
        self.write_text('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input',
                        self.password)

        # click login button
        self.click_element('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]/button/div')

        self.driver.implicitly_wait(5)

        try:
            self.driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div[3]/button[2]').click()

        except:
            pass

    def scroll(self, secs):

        start = time.time()

        while True:

            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            if time.time() - start > secs:
                break

    @property
    def infinite_scroll(self):

        self.last_height = self.driver.execute_script("return document.body.scrollHeight")

        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(3)

        self.new_height = self.driver.execute_script("return document.body.scrollHeight")

        if self.new_height == self.last_height:
            return True

        self.last_height = self.new_height

        return False

    def nav_user(self, user):

        self.driver.get(self.base_url + user)

    def click_element(self, xpath):
        element = self.driver.find_element(By.XPATH, xpath)
        ActionChains(self.driver).move_to_element(element).click(element).perform()

    def write_text(self, xpath, text):
        element = self.driver.find_element(By.XPATH, xpath)
        ActionChains(self.driver).move_to_element(element).send_keys_to_element(element, text).perform()

    def like_and_follow(self):

        # like
        self.driver.implicitly_wait(5)
        self.click_element('/html/body/div[4]/div[2]/div/article/div[2]/section[1]/span[1]/button')

        # follow
        self.driver.implicitly_wait(5)
        self.click_element('/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[2]/button')

        # if already following click CANCEL
        try:
            self.driver.implicitly_wait(5)
            self.click_element('/html/body/div[5]/div/div/div[3]/button[2]')
        except Exception:
            pass

    def comment(self, x, comments):

        # write comment
        self.driver.implicitly_wait(5)
        self.write_text('/html/body/div[4]/div[2]/div/article/div[2]/section[3]/div/form/textarea',
                        comments[x % len(comments)])

        # click comment button
        self.driver.implicitly_wait(5)
        self.click_element('/html/body/div[4]/div[2]/div/article/div[2]/section[3]/div/form/button')

    def close(self):
        try:
            self.driver.implicitly_wait(5)
            self.click_element('/html/body/div[4]/button[1]')
        except Exception:
            try:
                self.driver.implicitly_wait(5)
                element = self.driver.find_element(By.CLASS_NAME, 'ckWGn')
                ActionChains(self.driver).move_to_element(element).click(element).perform()
            except Exception:
                pass

    def activity(self, tags, comments, secs):

        with open('to_unfollow.txt', 'a') as f:

            for tag in tags:

                try:

                    self.driver.get(self.base_url + 'explore/tags/' + tag)

                    self.scroll(secs)

                    self.driver.implicitly_wait(5)
                    elements = self.driver.find_elements(By.CLASS_NAME, 'eLAPa')
                    print(len(elements))
                    counter = 0

                    while counter != len(elements):

                        for x in range(len(elements)):
                            time.sleep(15)

                            # click photo
                            self.driver.implicitly_wait(5)
                            ActionChains(self.driver).move_to_element((elements[x])).click((elements[x])).perform()

                            time.sleep(10)

                            # save username
                            self.driver.implicitly_wait(10)
                            f.write(self.driver.find_element(By.CLASS_NAME, 'e1e1d').text + '\n')

                            time.sleep(10)

                            # like and follow
                            self.like_and_follow()

                            time.sleep(10)

                            # comment
                            # self.comment(x, comments)

                            time.sleep(15)

                            # close
                            self.close()

                            counter += 1

                    pass

                except StaleElementReferenceException:
                    pass

    def unfollow(self):

        with open('unfollow.txt') as f:

            for user in f.readlines():

                try:

                    self.driver.get(self.base_url + user)
                    self.driver.implicitly_wait(5)
                    self.click_element('//*[@id="react-root"]/section/main/div/header/section/div[1]/div['
                                       '1]/span/span[1]/button[normalize-space()="Obserwowanie"]')
                    self.driver.implicitly_wait(5)
                    self.click_element('/html/body/div[4]/div/div/div[3]/button[1]')
                    time.sleep(2)
                    self.driver.implicitly_wait(8)

                except Exception as err:

                    print(err)
                    pass

    @staticmethod
    def download_image(src, image_filename, folder):

        folder_path = './{}'.format(folder)
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)

        img_filename = 'image_{}.jpg'.format(image_filename)
        print(img_filename)
        urllib.request.urlretrieve(src, '{}/{}'.format(folder, img_filename))

    def download_user_images(self, users):

        for user in users:

            self.nav_user(user)

            img_srcs = []
            finished = False

            while not finished:
                finished = self.infinite_scroll  # scroll down

                img_srcs.extend(
                    [img.get_attribute('src') for img in self.driver.find_elements(By.CLASS_NAME, 'FFVAD')])

            img_srcs = list(set(img_srcs))

            for idx, src in enumerate(img_srcs):
                self.download_image(src, idx, user)


if '__main__' == __name__:

    bot = IGbot('your_username', 'your_password')
    
    bot.download_user_images(['instagram'])

    bot.activity(['business', 'nature'],[''],5)
