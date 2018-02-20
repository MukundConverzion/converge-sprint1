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
        cur.execute("INSERT INTO comments(type,commentername,commenterdesignation,commenterprofileurl,comment,articleID,articleurl) VALUES (%s, %s, %s, %s, %s, %s, %s)",('Article',article['Commenter'],article['Commenter'],article['Commenter_url'],article['Comment'],article['ArticleId'],article['Articleurl']))
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
            cur.execute("select id,url from article")
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
    
            
    def getComments(self,url):
        driver = self.driver
        # for i in urls:
        driver.get(url)
        driver.implicitly_wait(8)
        time.sleep(4)
        body = driver.find_element_by_tag_name('body')
        comments = []
        while True:
            print("Scrolling..")
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(2)
            while len(driver.find_elements_by_xpath(".//button[@data-control-name='more_comments']")) > 0:
                print("Yes..")
                comment_button = WebDriverWait(driver,5).until(lambda driver:driver.find_element_by_xpath(".//button[@data-control-name='more_comments']"))
                # print(comment_button)
                action_comments = ActionChains(driver)
                action_comments.move_to_element(comment_button).click(comment_button).perform()
                time.sleep(5)
            body.send_keys(Keys.PAGE_DOWN)
            break

        comments_div = driver.find_element_by_class_name("feed-shared-comments-list")
        # print(comments_div.text)
        comments_divs = comments_div.find_elements_by_xpath(".//article")
        print(len(comments_divs))
            
        for div in comments_divs:
            time.sleep(3)    
            commenter_url_element = div.find_element_by_xpath(".//div[2]/a[2]")
            commenter_url = commenter_url_element.get_attribute("href")
            commenter = commenter_url_element.text
            comment_element = div.find_element_by_xpath(".//p[@dir='ltr']")
            comment_text = comment_element.text


            i_comment = {'commenter': commenter, 'commenter_url': commenter_url, 'comment_text': comment_text}
            comments.append(i_comment)

        #for i in comments:
        	#print(i['commenter'], i['commenter_url'], i['comment_text'])

        print("\n")
        print(len(comments))
        Linkedin.quitDriver(self)
        return comments
        
            
    def quitDriver(self):
        driver = self.driver
        driver.quit()



records=Linkedin.readdb()   
for x in range(0,len(records)):
    article = Linkedin()
    article.login()
    Comments=article.getComments(records[x][1])
    for y in range(0,len(Comments)):
        Table3={'Type':'Article','Commenter':Comments[y]['commenter'],'Commenter_url':Comments[y]['commenter_url'],'Comment':Comments[y]['comment_text'],'ArticleId':records[x][0],'Articleurl':records[x][1]}
        print(Table3)
        Linkedin.writedb(Table3)
            
        
    