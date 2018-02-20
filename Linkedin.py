import time
import requests
import os
import csv
import json
from bs4 import BeautifulSoup

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



    # Get recent activities, includes likes, shares etc.
    def getActivities(self, url):
        driver = self.driver
        try:
            
            # Enter activity page
            driver.get(url + "detail/recent-activity/")
            driver.implicitly_wait(5)
            

        except Exception as e:
            print(e)


    # Get articles
    def getArticles(self):
        driver = self.driver
        # Scroll to bottom to load the page fully
        driver.get(driver.current_url+"detail/recent-activity/posts/")
        time.sleep(2)

        try:

            if len(driver.find_elements_by_class_name("no-content")) > 0:
                print("No articles yet..")
            else:
                print("Articles found ...")
                # Scroll down once to get the articles
                # Keep it 5 scrolls for now
                # self.scrollToN(5)
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
                        if len(WebDriverWait(driver, 10).until(lambda driver:artpage.find_elements_by_class_name('feed-base-likes-list'))) > 0:
                            like_section = WebDriverWait(driver, 10).until(lambda driver:artpage.find_element_by_class_name('feed-base-likes-list'))
                            print(like_section)
                            n_likes = like_section.find_element_by_tag_name('h3').text
                            print(n_likes)
                            article_i['likes'] = n_likes
                        else:
                            print("No likes yet..")

                    except Exception as e:
                        print(e)
                            # Will work on the modal later, not working now

                            # section_likes = article.find_element_by_xpath(".//section[@data-control-name='likes']")
                            # print(" Likes for this article exist.")
                            # # Look for more_button
                            # if len(section_likes.find_elements_by_tag_name(".//button")) > 0:
                            #     more_button = section_likes.find_element_by_tag_name(".//button").click()
                            #     time.sleep(2)
                            #     likes_modal = driver.find_element_by_tag_name('artdeco-modal-content')
                            #     likes = likes_modal.find_elements_by_xpath(".//ul/li")
                            #     for like in likes:
                            #         print(like.text)
                            # else:
                            #     likes = section_likes.find_elements_by_xpath(".//ul/li")
                            #     for like in likes:
                            #         print(like.text)

                    
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

                    article_i['comments'] = comments
                    print(comments)
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
            
            
            



    # Get posts
    def getPosts(self):
        driver = self.driver
        # Scroll to bottom to load the page fully
        driver.get(driver.current_url+"detail/recent-activity/shares/")
        # self.scrollToBottom()
        time.sleep(2)
        
        try: 
            if len(driver.find_elements_by_class_name("no-content")) > 0:
                print("No posts yet.. ")
            else:
                print("Posts found...")
                posts_div = driver.find_element_by_id("voyager-feed")
                # print(posts_div)
                articles = posts_div.find_elements_by_xpath(".//article")
                print(len(articles))

                articles_list = []

                for article in articles[:2]:
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
                    # To be worked in the next iteration
                    
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

                        print("\n")
                        print(len(comments))

                        article_i['comments'] = comments
                        print(comments)

                    articles_list.append(article_i)

                print(articles_list)
                return(articles_list)



        except Exception as e:
            ex_type, ex, tb = sys.exc_info()
            print(traceback.print_tb(tb))
            print(e)



    # Get summary
    def getSummary(self):
        driver = self.driver
        # Look for see more, return expanded summary if present
        try:
            if driver.find_element_by_xpath("//button[@aria-controls='top-card-summary-treasury']"):
                summary_more_element = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath("//button[@aria-controls='top-card-summary-treasury']"))
                action_summary = ActionChains(driver)
                action_summary.move_to_element(summary_more_element).click().perform()
                time.sleep(3)

                summary_element = driver.find_element_by_class_name("pv-top-card-section__summary")

            else:
                summary_element = driver.find_element_by_class_name("pv-top-card-section__summary")

        except Exception as e:
            print(e)
            return ''
        else:
            summary = summary_element.text
            print(summary)
            return summary


    # Get experience
    def getExperience(self):
        driver = self.driver 
        try:
            exp_elements = driver.find_elements_by_xpath("//section[@class='experience-section']/ul/li")
            print(exp_elements)
        except Exception as e:
            print(e)
            return ''
        else:
            experiences = [i.text for i in exp_elements]
            print(experiences)
            return experiences
    

    # Get skills
    def getSkills(self):
        driver = self.driver
        # self.scrollToBottom()
        # Check for additional skills, extract them if present
        wait = WebDriverWait(driver, 5)
        
        while True:
            try:
                additional_skills = wait.until(lambda driver:driver.find_element(By.XPATH, "//button[@data-control-name='skill_details']"))
                print(additional_skills)
                action_skills = ActionChains(driver)
                action_skills.move_to_element(additional_skills).click().perform()
                time.sleep(3)

                skill_elements = wait.until(lambda driver:driver.find_element_by_class_name("pv-featured-skills-list"))
                skill_elements = skill_elements.find_elements_by_xpath(".//ul/li")

                additional_skill_elements = wait.until(lambda driver:driver.find_element_by_id("featured-skills-expanded"))
                additional_skill_elements = additional_skill_elements.find_elements_by_xpath(".//ul/li")

                total_skills = [i.text for i in skill_elements] + [j.text for j in additional_skill_elements]
                return total_skills
                print(total_skills)
                break

            except Exception as e:
                print(e)
                body = driver.find_element_by_tag_name('body')
                print("Scrolling..")
                body.send_keys(Keys.PAGE_DOWN)
                time.sleep(2)

        

    # Get education details
    def getEducation(self):
        driver = self.driver
        try:
            edu_elements = driver.find_elements_by_xpath("//section[@class='education-section']/ul/li")
        except Exception as e:
            print(e)
            return ''
        else:
            edus = [i.text for i in edu_elements]
            print(edus)
            return edus


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



    def quitBrowser(self):
        driver = self.driver
        driver.quit()

    def gotoProfile(self, url):
        driver = self.driver
        driver.get(url)
        print("Entering profile ...")
        time.sleep(8)



def writeToFile(objects):
    with open('connections.txt', 'w') as file:
        file.write(json.dumps(objects))


def main():
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
    posts = linkedin.getPosts()
        #Extracting overview details using regex and create a dictionary to push into a pandas dataframe
        #regex = r"\n"
        #matches = re.finditer(regex,overview[0])
        #listIndex=[]
        #for match in matches:
            #listIndex_1=[]
            #listIndex_1.append(match.start())
            #listIndex_1.append(match.end())
            #print (listIndex_1)
            #listIndex.append(listIndex_1)
        #Name = overview[0][0:listIndex[0][0]]
        #Designation_current = overview[0][listIndex[2][1]:listIndex[3][0]]
        #Followers_Count = overview[1].replace(" followers","")
        #Table1 ={'Name':Name, 'Current Designation':Designation_current,'Followers count':Followers_Count}
        #print (Table1)
        # linkedin.getArticles()
        # linkedin.getSummary()
        #Posts=linkedin.getPosts()
        #for x in range(0,len(Posts)):
            #if(len(Posts[x])!=3):
                #del Posts[x]
        #for i in range(0,len(Posts)):
            #Table5 = {'Posted by':test_name,'Content': Posts[i]['content'],'Like':Posts[i]['like'],'time':Posts[i]['time']}       
            #print (Table5)
        # linkedin.getExperience()
        # linkedin.getSkills()
        # linkedin.getEducation()
        #all_articles = linkedin.getArticles()
        #for i in range(0,len(all_articles)):
            #Table3={'Posted by':test_name,'Article title':all_articles[i]['title'],'Article Likes':all_articles[i]['likes'],'Time':all_articles[i]['time'],'Url':all_articles[i]['url'],'Content':all_articles[i]['content']}
            #print (Table3)
        #all_cons=linkedin.getConnections()
        #connections=list(all_cons.keys())
        #Url=list(all_cons.values())
        # for i in range(1,len(connections)):
        #    connections=Connections[i].split('\n')
        #    Name = connections[0]
        #    Connection_Type = connections[1]
        #    Table2={'Name':test_name,'Connection_Name':Name,'Profile_Link':Url[i],'Connection_Type':Connection_Type}
        #    print (Table2)
        #print (Table2)
        # writeToFile(all_cons)
        # write connections data to file 
        # linkedin.gotoProfile(test_url)
        # overview = linkedin.getOverview()
        # activities = linkedin.getActivities()
        # summary = linkedin.getSummary()
        # experiences = linkedin.getExperience()
        # skills = linkedin.getSkills()
        # education = linkedin.getEducation()

