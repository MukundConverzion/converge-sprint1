import time
import requests
import os
import csv
import json
from bs4 import BeautifulSoup
import psycopg2
import sys
import pprint

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
chrome_options = Options()  
chrome_options.add_argument("--headless")  

class Linkedin:
    def __init__(self, ):
        # options = webdriver.ChromeOptions()
        # Replace the dir with the profile of your google chrome
        # To do this, goto google-chrome, and type: chrome://version, and get the profile path
        # Also make sure to clear all caches before starting
        # options.add_argument('user-data-dir=/home/dipes/.config/google-chrome/Profile')
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.driver.maximize_window()
        self.email = 'mukundkrishnaravi@hotmail.com'
        self.password = 'klow231991'
        
    def writedb(article):
            conn_string = "host='localhost' dbname='Converge' user='postgres' password='123456789'"
            print ("Connecting to database\n	->%s" % (conn_string))
            # get a connection, if a connect cannot be made an exception will be raised here
            # conn.cursor will return a cursor object, you can use this cursor to perform queries
            conn = psycopg2.connect(conn_string)
            cur = conn.cursor()
            #print(cursor)
            #cur.execute("CREATE TABLE influencer_1 (id serial PRIMARY KEY, num integer, data varchar);")
            cur.execute("INSERT INTO article(title,content,url,likes) VALUES (%s, %s, %s,%s)",(article['Article title'],article['Content'],article['Url'],article['likes']))
            conn.commit()
            #cur.execute("SELECT * FROM influencers;")
            #records = cur.fetchall()
            #pprint.pprint(records)
            print ("Connected!\n")        
    def readdb(): 
            conn_string = "host='localhost' dbname='Converge' user='postgres' password='123456789'"
            print ("Connecting to database\n	->%s" % (conn_string))
            # get a connection, if a connect cannot be made an exception will be raised here
            # conn.cursor will return a cursor object, you can use this cursor to perform queries
            conn = psycopg2.connect(conn_string)
            cur = conn.cursor()
            #print(cursor)
            #cur.execute("CREATE TABLE influencer_1 (id serial PRIMARY KEY, num integer, data varchar);")
            cur.execute("select name,article_url from influencernew where name='Leza Parker'")
            records = cur.fetchall()
            return records

    
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
    
    def gotoProfile(self, url):
        driver = self.driver
        driver.get(url)
        print("Entering profile ...")
        time.sleep(8)
    
    def getArticles(self):
        driver = self.driver
        # Scroll to bottom to load the page fully
        driver.get(driver.current_url)
        time.sleep(2)

        try:

            if len(driver.find_elements_by_class_name("no-content")) > 0:
                print("No articles yet..")
            else:
                print("Articles found ...")
                # Scroll down once to get the articles
                # Keep it 5 scrolls for now
                # self.scrollToN(50)
                articles = driver.find_elements_by_tag_name('article')
                print (articles)

                articles_list = []

                for article in articles:
                    article_i = {}
                    if len(article.find_elements_by_class_name('pv-post-entity__title')) > 0:
                        title = article.find_element_by_class_name('pv-post-entity__title').text
                        print(title)
                        article_i['title'] = title
                    

                    if len(article.find_elements_by_xpath(".//time")) > 0:
                        timestamp = article.find_element_by_xpath(".//time").text
                        print(timestamp)
                        article_i['time'] = timestamp

                    a = article.find_element_by_tag_name("a")
                    url = a.get_attribute('href')
                    article_i['url']  = url
                    print(url)

                    actions = ActionChains(driver)
                    actions.key_down(Keys.CONTROL).click(a).key_up(Keys.CONTROL).perform()
                    time.sleep(3)
                    driver.switch_to.window(driver.window_handles[-1])
                    time.sleep(2)
                    self.scrollToBottom()
                    
                    
                    artpage = driver.find_element_by_tag_name('article')
                    content = artpage.find_element_by_class_name('reader-article-content').text
                    print(content)
                    article_i['content'] = content

                    time.sleep(3)
                    # Extract likes
                    try:
                        if len(WebDriverWait(driver, 10).until(lambda driver:artpage.find_elements_by_class_name('feed-shared-likes-list'))) > 0:
                            like_section = WebDriverWait(driver, 10).until(lambda driver:artpage.find_element_by_class_name('feed-shared-likes-list'))
                            print(like_section)
                            n_likes = like_section.find_element_by_tag_name('h3').text
                            print(n_likes)
                            article_i['likes'] = n_likes
                        else:
                            print("No likes yet..")

                    except Exception as e:
                        print(e)
                    time.sleep(2)

                        # Extract comments
                    comments = []

                    # To be worked in another iteration
                    # if len(artpage.find_elements_by_xpath(".//button[@data-control-name='more_comments']")) > 0:
                    #     comment_button = WebDriverWait(driver,10).until(lambda driver:artpage.find_element_by_xpath(".//button[@data-control-name='more_comments']"))
                    #     action_comments = ActionChains(driver)
                    #     action_comments.move_to_element(comment_button).click().perform()
                    # time.sleep(4)

                    # comments_divs = WebDriverWait(driver, 10).until(lambda driver:artpage.find_elements_by_xpath(".//article"))
                    # print(comments_divs)
                    
                    # for comment in comments_divs:
                    #     comments.append(comment.text)

                    #article_i['comments'] = comments
                    #print(comments)
                    articles_list.append(article_i)

                    driver.close()
                    driver.switch_to_window(driver.window_handles[0])

                print(articles_list)
                return (articles_list)
                
                    # article_i['title'] = title
                    # article_i['time'] = timestamp
                    # article_i['url'] = url

                    # Go to url to get full article, likes and comments

        except Exception as e:
            ex_type, ex, tb = sys.exc_info()
            print(traceback.print_tb(tb))
            print(e)
            
    def scrollToN(self, n_scrolls):
        # Time to pause for the page to load
        SCROLL_PAUSE_TIME = 2

        driver = self.driver
        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight;")

        for i in range(n_scrolls):
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)
            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight;")
            if new_height == last_height:
                break
            last_height = new_height 
            
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
            
#def main():
records=Linkedin.readdb()
test_name = records[0][0]
test_url = records[0][1]
linkedin = Linkedin()
linkedin.login()
linkedin.gotoProfile(test_url)
all_articles = linkedin.getArticles()
for i in range(0,len(all_articles)):
    article={'Posted by':test_name,'Article title':all_articles[i]['title'],'Time':all_articles[i]['time'],'Url':all_articles[i]['url'],'Content':all_articles[i]['content'],'likes':all_articles[i]['likes']}
    Linkedin.writedb(article)
        
    
    

    
    
    
    