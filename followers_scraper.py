import sys
import pickle
import time
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#CHANGE THIS PARAMETERS
instagram_username = "INSTAGRAM_USERNAME" #WITHOUT @
instagram_password = "INSTAGRAM_PASSWORD"

#FUNCTION TO REMOVE HTML TAGS FROM STRINGS
TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(text):
    return TAG_RE.sub('', text)

#CHECK ARGVS/LENGTH
if len(sys.argv) <= 1 or (sys.argv[1] != 'login' and sys.argv[1] != 'scrape'):
    print("Missing parameter, use: python " + sys.argv[0] + " scrape|login")
    sys.exit(0)

#START SELENIUM 
driver = webdriver.Chrome(executable_path='chromedriver.exe')
driver.set_window_size(375, 667)

if sys.argv[1] == 'login':
    #GO ON INSTAGRAM LOGIN AND MAKE LOGIN
    driver.get('https://www.instagram.com/accounts/login/')
    time.sleep(2)
    driver.find_element_by_xpath("//input[@aria-label='Numero di telefono, nome utente o e-mail']").send_keys(instagram_username)
    driver.find_element_by_xpath("//input[@aria-label='Password']").send_keys(instagram_password)
    driver.find_element_by_xpath("//div[@class='                    Igw0E     IwRSH      eGOV_         _4EzTm    bkEs3                          CovQj                  jKUp7          DhRcB                                                    ']").click()
    time.sleep(2)
    #SAVE COOKIE FOR FUTURE LOGINS
    driver.get('https://www.instagram.com/' + instagram_username)
    pickle.dump(driver.get_cookies() , open('cookies.pkl', 'wb'))
    driver.close()
    print("Login cookies have been saved, now use: python " + sys.argv[0] + " scrape")
    sys.exit(0)
elif sys.argv[1] == 'scrape':
    #GO ON INSTAGRAM LOGIN AND LOAD THE PREVIOUS COOKIES
    driver.get('https://www.instagram.com/accounts/login/')
    cookies = pickle.load(open('cookies.pkl','rb'))
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.get('https://www.instagram.com/accounts/activity/?__a=1&include_reel=true')
    time.sleep(1)
    #SAVE JSON WITH FOLLOWERS LIST
    f = open('follower_list.json','w+')
    f.write(remove_tags(driver.page_source))
    f.close()
    driver.close()
    print("The list of the latest followers has been written in: follower_list.json")
    sys.exit(0)
else:
    #USELESS ERROR (ARGVS CHECK BEFORE) xD
    print('OPS ... something went wrong! Contact the developer.')
    sys.exit(0)