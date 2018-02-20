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
            
    def writedb(article):
        conn_string = "host='localhost' dbname='Converge' user='postgres' password='123456789'"
        print ("Connecting to database\n	->%s" % (conn_string))
        # get a connection, if a connect cannot be made an exception will be raised here
        # conn.cursor will return a cursor object, you can use this cursor to perform queries
        conn = psycopg2.connect(conn_string)
        cur = conn.cursor()
        #print(cursor)
        #cur.execute("CREATE TABLE influencer_1 (id serial PRIMARY KEY, num integer, data varchar);")
        cur.execute("INSERT INTO connection(name,connectionname,link_url,connection_type) VALUES (%s, %s, %s,%s)",(article['Name'],article['Connection_Name'],article['Profile_Link'],article['Connection_Type']))
        conn.commit()
        #cur.execute("SELECT * FROM influencers;")
        #records = cur.fetchall()
        #pprint.pprint(records)
        print ("Connected!\n")        


    
    # Get connections
    def getConnections(self):
        driver = self.driver
        # find see_all_connections

        driver.implicitly_wait(8)               


        try:
            all_conn_element = driver.find_element_by_xpath("//a[@data-control-name='view_all_connections']")
        except Exception as e:
            print(e)
        else:
            all_conn = all_conn_element.click()
            time.sleep(4)
            print("Browsing connections..")
            
            allConnections = {} 

            # First scroll down to the bottom to load the page fully
            self.scrollToBottom()

            try:
                # Treat the active tab differently, and then loop for the remaining numbers
                # The first page
                profiles = WebDriverWait(driver, 10).until(lambda driver: driver.find_elements_by_xpath("//a[@data-control-name='search_srp_result']"))
                # print(profiles)
                for i in profiles:
                    display_name = i.text
                    print(display_name)
                    profile_link = i.get_attribute('href')
                    allConnections[display_name] = profile_link

            except Exception as e:
                print(e)

            else:
                while(True):
                    try: 
                        next_element = driver.find_element_by_xpath("//button[@class='next']")
                        # print(next_element)
                        actions = ActionChains(driver)
                        actions.move_to_element(next_element).click().perform()
                        # Now loop for the remaining pages
                        # Skip the first pages
                    except Exception as e:
                        print(e)
                        print("Reached the end of the paginator...")
                        return allConnections

                    else:
                        # don't know if the url changes
                        # again repeat the things done for the first page
                        time.sleep(5)
                        driver.get(driver.current_url)
                        self.scrollToBottom()
                        driver.implicitly_wait(10)

                        profiles_loop = WebDriverWait(driver, 10).until(lambda driver: driver.find_elements_by_xpath("//a[@data-control-name='search_srp_result']"))
                        for j in profiles_loop:
                            display_name_j = j.text
                            print(display_name_j)
                            profile_link_j = j.get_attribute('href')
                            allConnections[display_name_j] = profile_link_j

                
                print(allConnections)
                print("No. of connections: ", len(allConnections))
                return allConnections
            
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



    def quitBrowser(self):
        driver = self.driver
        driver.quit()
        
    def gotoProfile(self, url):
        driver = self.driver
        driver.get(url)
        print("Entering profile ...")
        time.sleep(8)
        


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
test_name = test_names[4]
test_url = test_urls[4]
linkedin = Linkedin()
linkedin.login()
linkedin.gotoProfile(test_url)
all_cons=linkedin.getConnections()
Connections=list(all_cons.keys())
Url=list(all_cons.values())
for i in range(1,len(Connections)):
    connections=Connections[i].split('\n')
    Name = connections[0]
    Connection_Type = connections[1]
    Table2={'Name':test_name,'Connection_Name':Name,'Profile_Link':Url[i],'Connection_Type':Connection_Type}
    print (Table2)
Linkedin.writedb(Table2)    
    

