from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import os
import shutil

try:
    shutil.rmtree('./profiles/*')
except:
    pass


chromedriver = "./chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
print "3"
browser = webdriver.Chrome(chromedriver) 
print "4"
browser.get('http://24ur.com')

links = browser.find_elements_by_xpath("//a")

print links
print "5"
browser.quit()


