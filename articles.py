import time
import requests
import os
import csv
import json

# Import selenium reqs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import re
import traceback
import sys

urls = ['https://www.linkedin.com/pulse/rise-india-one-big-stories-asia-next-20-years-piyush-gupta/',
                'https://www.linkedin.com/pulse/future-banking-piyush-gupta/',
                'https://www.linkedin.com/pulse/belt-road-initiative-implications-asia-singapore-piyush-gupta/',
                'https://www.linkedin.com/pulse/what-trump-led-us-augurs-asia-markets-year-piyush-gupta/',
                'https://www.linkedin.com/pulse/why-im-keeping-faith-china-piyush-gupta/',
        ]


class Linkedin:
    '''
    Initialize necessary variables
    This one works for the non-public profiles
    Requires login
    '''
    def __init__(self, ):
        # options = webdriver.ChromeOptions()
        # Replace the dir with the profile of your google chrome
        # To do this, goto google-chrome, and type: chrome://version, and get the profile path
        # Also make sure to clear all caches before starting
        # options.add_argument('user-data-dir=/home/dipes/.config/google-chrome/Profile')
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.email = ''
        self.password = ''


    def login(self):
        driver = self.driver
        url = 'https://www.linkedin.com/'
        try:
            driver.get(url)
            emailFieldElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id('login-email') )
            passwordFieldElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id('login-password')) 
            loginbutton = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id('login-submit'))
        except Exception as e:
            print(e)
            print('Error in elements for login...')
        else:
            emailFieldElement.send_keys(self.email)
            time.sleep(2)
            passwordFieldElement.send_keys(self.password)
            time.sleep(2)
            loginbutton.click()
            print('Logging in...')
            time.sleep(3)


    def scrollToBottom(self):
        # Time to pause for the page to load
        SCROLL_PAUSE_TIME = 2

        driver = self.driver
        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight;")

        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)
            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight;")
            if new_height == last_height:
                break
            last_height = new_height

    
    def getComments(self):
        driver = self.driver
        
        # for i in urls:
        driver.get(urls[0])
        driver.implicitly_wait(8)
        time.sleep(4)

        body = driver.find_element_by_tag_name('body')
        comments = []
        while True:
            print("Scrolling..")
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(2)
            if len(driver.find_elements_by_xpath(".//button[@data-control-name='more_comments']")) > 0:
                print("Yes..")
                comment_button = WebDriverWait(driver,5).until(lambda driver:driver.find_element_by_xpath(".//button[@data-control-name='more_comments']"))
                print(comment_button)

                action_comments = ActionChains(driver)
                action_comments.move_to_element(comment_button).click(comment_button).perform()
                time.sleep(3)
                body.send_keys(Keys.PAGE_DOWN)
                break

        comments_div = driver.find_element_by_class_name("feed-base-comments-list")
        comments_divs = comments_div.find_elements_by_xpath(".//article")
        print(comments_divs)
            
        for div in comments_divs:
            
            commenter_url_element = div.find_element_by_xpath("//div[2]/a[2]")
            commenter_url = commenter_url_element.get_attribute('href')
            commenter = commenter_url_element.text
            comment_text = div.find_element_by_xpath("//div[@class='feed-base-comment-item-content-body']").text
            i_comment = {'commenter': commenter, 'commenter_url': commenter_url, 'comment_text': comment_text}
            comments.append(i_comment)

        print(comments)
            
    def quitDriver(self):
        driver = self.driver
        driver.quit()


article = Linkedin()
article.login()
article.getComments()
# article.quitDriver()

