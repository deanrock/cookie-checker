from model import *
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =  config.DB_URI
app.config['SQLALCHEMY_POOL_RECYCLE'] = 3600
app.secret_key = config.secret_key



db.init_app(app)

def check_cookies(t):

	print t.domain

	os.system("killall -9 firefox")

	browser = webdriver.Firefox(webdriver.FirefoxProfile(profile_directory='C:/Users/Dejan/Desktop/cookie-checker/profile'))
	
	browser.delete_all_cookies()

	t.status = 2
	db.session.commit()

	try:
		browser.get(t.domain)
	except:
		t.status = 3
		t.info = 'Wrong URL! Task Aborted'
		db.session.commit()
		return

	cookies = browser.get_cookies()

	for co in cookies:
		c = Cookie()
		c.test_id = t.id
		c.name = co['name']
		c.domain = co['domain']
		c.value = co['value'][:200]

		db.session.add(c)

	t.status = 3
	db.session.commit()

	browser.close()

if __name__ == '__main__':

	while True:
		ctx = app.test_request_context()
		ctx.push()
		t = Test.query.filter(Test.status==1).first()

		if t:
			try:
				check_cookies(t)
			except:
				t.status = 3
				t.info = "Error! Please try again!"
				
				db.session.commit()
		else:
			sleep(1)

		ctx.pop()

	if browser:
		browser.close()
