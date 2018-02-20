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
chrome_options = Options()  
chrome_options.add_argument("--headless")  

import traceback
import sys
#chrome_options = Options()  
#chrome_options.add_argument("--headless")  



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
    
    
            
    def writedb(influencer):
            conn_string = "host='localhost' dbname='Converge' user='postgres' password='123456789'"
            print ("Connecting to database\n	->%s" % (conn_string))
            # get a connection, if a connect cannot be made an exception will be raised here
            # conn.cursor will return a cursor object, you can use this cursor to perform queries
            conn = psycopg2.connect(conn_string)
            cur = conn.cursor()
            #print(cursor)
            #cur.execute("CREATE TABLE influencer_1 (id serial PRIMARY KEY, num integer, data varchar);")
            cur.execute("INSERT INTO influencernew (Name,Profile_Url,Followers,Designation,Postpage_Url,Article_Url) VALUES (%s, %s, %s, %s, %s, %s)",(influencer['Name'],influencer['Profile_url'],influencer['Followers count'],influencer['Current Designation'],influencer['Posts_Url'],influencer['Articles_Url']))
            conn.commit()
            #cur.execute("SELECT * FROM influencers;")
            #records = cur.fetchall()
            #pprint.pprint(records)
            print ("Connected!\n")
            
    # Get the basic details, name, address, no. of followers
    def getOverview(self):
        driver = self.driver

        try:
            overview_element = driver.find_element_by_class_name('pv-top-card-section__information')
            follower_count = driver.find_element_by_class_name("pv-recent-activity-section__follower-count").text
            
        except Exception as e:
            print(e)
            return ''
        
        else:
            overview = overview_element.text
            print(overview)
            print (follower_count)
            return overview, follower_count
    
    def gotoProfile(self, url):
        driver = self.driver
        driver.get(url)
        print("Entering profile ...")
        time.sleep(8)
     
        
#def main():
profile_urls = {
            'Leza Parker': 'https://www.linkedin.com/in/leza-parker/',
            'Lim Hong Bin': 'https://www.linkedin.com/in/lim-hong-bin-0299542b/',
            'Dean Reinhard': 'https://www.linkedin.com/in/deanreinhard/',
            'James Nicol': 'https://www.linkedin.com/in/jamesnicol/',
            'mingjie (mj) xu': 'https://www.linkedin.com/in/mingjiexu/',
            'Lisa Luk': 'https://www.linkedin.com/in/lisaluk/',
            'Shaurya Sinha': 'https://www.linkedin.com/in/shaurya157/',
            'Zhang Xuan': 'https://www.linkedin.com/in/zhang-xuan-82533a129/',
            'Jasmine Nicholls (nee Lee)': 'https://www.linkedin.com/in/jasmine-nicholls-nee-lee-aba68530/',
            'Mukund Krishna Ravi': 'https://www.linkedin.com/in/mukundkrishnaravi/',
            'Annette Tilbrook': 'https://www.linkedin.com/in/annettetilbrook/',
            'Sean Straton': 'https://www.linkedin.com/in/sean-straton-31a46689/',
            'Piyush Gupta': 'https://www.linkedin.com/in/piyushguptadbs/',
            'Xavier Chia': 'https://www.linkedin.com/in/xavierchia/',
            'Yijun Du': 'https://www.linkedin.com/in/yijun-du-857a43118/',
            'Mahima Damani': 'https://www.linkedin.com/in/mahima-damani/',
            }
        # Try it with test_urls
test_urls = list(profile_urls.values())
test_names =list(profile_urls.keys())
test_name = test_names[1]
test_url = test_urls[1]
linkedin = Linkedin()
linkedin.login()
linkedin.gotoProfile(test_url)
overview=linkedin.getOverview()
    #Extracting overview details using regex and create a dictionary to push into a pandas dataframe
regex = r"\n"
matches = re.finditer(regex,overview[0])
listIndex=[]
for match in matches:
    listIndex_1=[]
    listIndex_1.append(match.start())
    listIndex_1.append(match.end())
    print (listIndex_1)
    listIndex.append(listIndex_1)
Name = overview[0][0:listIndex[0][0]]
Designation_current = overview[0][listIndex[2][1]:listIndex[3][0]]
Followers_Count = overview[1].replace(" followers","")
influencer ={'Name':Name, 'Current Designation':Designation_current,'Followers count':Followers_Count, 'Profile_url': test_url , 'Articles_Url':str(test_url)+"detail/recent-activity/posts/", 'Posts_Url':str(test_url)+"detail/recent-activity/shares/"}
#Writing basic information into the database 
Linkedin.writedb(influencer)
# Try it with test_urls
test_urls = list(profile_urls.values())
test_names =list(profile_urls.keys())
test_name = test_names[0]
test_url = test_urls[0]
linkedin = Linkedin()
linkedin.login()
linkedin.gotoProfile(test_url)
overview=linkedin.getOverview()
#Extracting overview details using regex and create a dictionary to push into a pandas dataframe
regex = r"\n"
matches = re.finditer(regex,overview[0])
listIndex=[]
for match in matches:

    listIndex_1=[]
    listIndex_1.append(match.start())
    listIndex_1.append(match.end())
    print (listIndex_1)
    listIndex.append(listIndex_1)
Name = overview[0][0:listIndex[0][0]]
Designation_current = overview[0][listIndex[2][1]:listIndex[3][0]]
Followers_Count = overview[1].replace(" followers","")
influencer ={'Name':Name, 'Current Designation':Designation_current,'Followers count':Followers_Count, 'Profile_url': test_url , 'Articles_Url':str(test_url)+"detail/recent-activity/posts/", 'Posts_Url':str(test_url)+"detail/recent-activity/shares/"}
#Writing basic information into the database 
Linkedin.writedb(influencer)
    
    
    
     
