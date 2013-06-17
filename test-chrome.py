from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import os
import shutil

try:
    shutil.rmtree('./profiles/*')
except:
    pass

print "1"
co = webdriver.ChromeOptions()
co.add_argument("--user-data-dir=./profiles")
print "2"
chromedriver = "./chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
print "3"
browser = webdriver.Chrome(chromedriver, chrome_options = co) 
print "4"
browser.get('http://24ur.com')
print "5"
browser.quit()


