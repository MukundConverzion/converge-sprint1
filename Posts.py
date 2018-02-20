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
            
    # Goto public profile
    def gotoProfile(self, url):
        driver = self.driver
        driver.get(url)
        print("Entering profile ...")
        time.sleep(8)
            
    def readdb(): 
        conn_string = "host='localhost' dbname='Converge' user='postgres' password='123456789'"
        print ("Connecting to database\n	->%s" % (conn_string))
        # get a connection, if a connect cannot be made an exception will be raised here
        # conn.cursor will return a cursor object, you can use this cursor to perform queries
        conn = psycopg2.connect(conn_string)
        cur = conn.cursor()
        #print(cursor)
        #cur.execute("CREATE TABLE influencer_1 (id serial PRIMARY KEY, num integer, data varchar);")
        cur.execute("select name,postpage_url from influencernew where name='Lim Hong Bin'")
        records = cur.fetchall()
        return records
    
    def writedb(article):
        conn_string = "host='localhost' dbname='Converge' user='postgres' password='123456789'"
        print ("Connecting to database\n	->%s" % (conn_string))
        # get a connection, if a connect cannot be made an exception will be raised here
        # conn.cursor will return a cursor object, you can use this cursor to perform queries
        conn = psycopg2.connect(conn_string)
        cur = conn.cursor()
        #print(cursor)
        #cur.execute("CREATE TABLE influencer_1 (id serial PRIMARY KEY, num integer, data varchar);")
        cur.execute("INSERT INTO comments(type,commentername,commenterdesignation,commenterprofileurl,comment, postid) VALUES (%s, %s, %s, %s, %s, %s)",('Post',article['Commenter'],article['Commenter'],article['Commenter_url'],article['Comment'],article['Postid']))
        conn.commit()
        #cur.execute("SELECT * FROM influencers;")
        #records = cur.fetchall()
        #pprint.pprint(records)
        print ("Connected!\n")  
    
    def writedbPost(article):
        conn_string = "host='localhost' dbname='Converge' user='postgres' password='123456789'"
        print ("Connecting to database\n	->%s" % (conn_string))
        # get a connection, if a connect cannot be made an exception will be raised here
        # conn.cursor will return a cursor object, you can use this cursor to perform queries
        conn = psycopg2.connect(conn_string)
        cur = conn.cursor()
        #print(cursor)
        #cur.execute("CREATE TABLE influencer_1 (id serial PRIMARY KEY, num integer, data varchar);")
        cur.execute("INSERT INTO Posts(postid, postcomment, postlike) VALUES (%s, %s, %s)",(article['Postid'],article['PostContent'],article['Likes']))
        conn.commit()
        #cur.execute("SELECT * FROM influencers;")
        #records = cur.fetchall()
        #pprint.pprint(records)
        print ("Connected!\n")          
        
    # Get posts
    def getPosts(self):
        driver = self.driver
        # Scroll to bottom to load the page fully
        driver.get(driver.current_url)
        self.scrollToN(2)
        time.sleep(2)
        if len(driver.find_elements_by_class_name("no-content")) > 0:
                print("No posts yet.. ")
        else:
                print("Posts found...")
                posts_div = driver.find_element_by_id("voyager-feed")
                # print(posts_div)
                articles = posts_div.find_elements_by_xpath(".//article")
                print(len(articles))

                articles_list = []
                postid = 0
                for article in articles:    
                    article_i = {}
                    # Extract all details of the article
                    if len(article.find_elements_by_xpath(".//time")) > 0:
                        timestamp = article.find_element_by_xpath(".//time").text
                        print(timestamp)
                        article_i['time'] = timestamp

                    if len(article.find_elements_by_xpath(".//p")) > 0:
                        content = article.find_element_by_xpath(".//p").text
                        print(content)
                        article_i['content'] = content


                     # Check for likes and comments
                    if len(article.find_elements_by_xpath(".//button[@data-control-name='likes_count']")) > 0:
                        n_likes = article.find_element_by_xpath(".//button[@data-control-name='likes_count']").text

                        print(n_likes)
                    else:
                        n_likes = 0
                    article_i['like'] = n_likes

                    time.sleep(2)
                    wait = WebDriverWait(driver, 6)

                    comments = []
                    
                    if len(article.find_elements_by_xpath(".//button[@data-control-name='comments_count']")) > 0:
                        comment_button = wait.until(lambda driver:article.find_element_by_xpath(".//button[@data-control-name='comments_count']"))
                        action_comments = ActionChains(driver)
                        action_comments.move_to_element(comment_button).click().perform()
                        time.sleep(5)

                        while len(driver.find_elements_by_xpath(".//button[@data-control-name='more_comments']")) > 0:
                            print("Yes..")
                            comment_button = WebDriverWait(driver,5).until(lambda driver:driver.find_element_by_xpath(".//button[@data-control-name='more_comments']"))
                            # print(comment_button)

                            action_comments = ActionChains(driver)
                            action_comments.move_to_element(comment_button).click(comment_button).perform()
                            time.sleep(5)

                        comments_divs = article.find_elements_by_xpath(".//article")
                        print(comments_divs)
                        
                        print(len(comments_divs))
            
                        for div in comments_divs:
                            time.sleep(3)
                            
                            commenter_url_element = div.find_element_by_xpath(".//div/div/a")
                            commenter_url = commenter_url_element.get_attribute("href")
                            commenter = commenter_url_element.text
                            comment_element = div.find_element_by_xpath(".//p[@dir='ltr']")
                            comment_text = comment_element.text
                            i_comment = {'commenter': commenter, 'commenter_url': commenter_url, 'comment_text': comment_text}
                            comments.append(i_comment)

                        for i in comments:
                            print(i['commenter'], i['commenter_url'], i['comment_text'])
                            Table3={'Type':'Post','Commenter':i['commenter'],'Commenter_url':i['commenter_url'],'Comment':i['comment_text'],'Postid': postid}
                            Linkedin.writedb(Table3)  
                        print("\n")
                        print(len(comments))

                        article_i['comments'] = comments
                        #print(comments)
                    articles_list.append(article_i)
                    postid =postid + 1
                    Table4={'Postid':postid,'PostContent':article_i['content'],'Likes':article_i['like']} 
                    Linkedin.writedbPost(Table4)                         
                print(articles_list)
                Linkedin.quitDriver(self)
                return(articles_list)        

    def quitDriver(self):
        driver = self.driver
        driver.quit() 

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
                
#def main():
records=Linkedin.readdb()
test_name = records[0][0]
test_url = records[0][1]
linkedin = Linkedin()
linkedin.login()
linkedin.gotoProfile(test_url)
all_articles = linkedin.getPosts()   

      
                 
