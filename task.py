from model import *
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import os
import config as myconfig
import MySQLdb as mdb
from xvfbwrapper import Xvfb
import shutil
from urlparse import urlparse
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =  config.DB_URI
app.config['SQLALCHEMY_POOL_RECYCLE'] = 3600
app.secret_key = config.secret_key

db.init_app(app)

class get_cookies:
    def __init__(self):
        self.browser = None
        self.to_visit = []

    def __parse_cookies(self, url):
        print "parse %s" % url

        #socket.setdefaulttimeout(2)
        self.browser.set_page_load_timeout(3)
        self.browser.get(url)

        u = Url()
        u.test_id = t.id
        u.url = self.url
        u.datetime = datetime.datetime.now()
        
        db.session.add(u)
        db.session.commit()
        print "bc"
        cookies = self.browser.get_cookies()
        print "ac"
        for co in cookies:
            c = Cookie()
            c.url_id = u.id
            c.name = co['name']
            c.domain = co['domain']
            c.value = co['value'][:200]

            if 'expiry' in co:
                c.expires = co['expiry']

            db.session.add(c)

        db.session.commit()

    def check_cookies(self, t):
        t.status = 2
        db.session.commit()

        vdisplay = Xvfb()
        vdisplay.start()

        #chrome options
        #co = webdriver.ChromeOptions()
        #co.add_argument("--user-data-dir=./profiles")

        chromedriver = "./chromedriver"
        os.environ["webdriver.chrome.driver"] = chromedriver

        #browser = webdriver.Chrome(chromedriver, chrome_options = co)
        self.browser = webdriver.Chrome(chromedriver)
        self.browser.delete_all_cookies()

        #visit first page
        self.url = t.domain
        """try:
            self.browser.get(self.url)
        except:
            t.status = 4
            t.info = 'Wrong URL! Task Aborted'
            db.session.commit()

            vdisplay.stop()
            return
            """

        self.__parse_cookies(t.domain)

        domain = urlparse(t.domain).netloc

        links = self.browser.find_elements_by_tag_name("a")

        random.shuffle(links)

        for link in links:
            u = urlparse(link.get_attribute('href'))

            print u.netloc
            if u.netloc == domain and link.get_attribute('href') != self.url:
                print link.get_attribute('href')
                self.to_visit.append(link.get_attribute('href'))

                if len(self.to_visit) == 3:
                    break
        
        for link in self.to_visit:
            self.__parse_cookies(link)

        print t.domain

        

        #finish
        t.status = 3
        t.finished = datetime.datetime.now()
        db.session.commit()

        self.browser.close()
        vdisplay.stop()

if __name__ == '__main__':

    while True:
        ctx = app.test_request_context()
        ctx.push()
        t = Test.query.filter(Test.status==1).first()

        if t:
            gc = get_cookies()
            gc.check_cookies(t)
            print "hext"
            #try:
            #    check_cookies(t)
            #except Exception,e:
            #    print str(e)
            #    t.status = 4
            #    t.info = "Please try again!"
            #
            #   db.session.commit()
        else:
            sleep(1)

        ctx.pop()

    if browser:
        browser.close()
