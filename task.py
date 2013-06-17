from model import *
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import os
import config as myconfig
import MySQLdb as mdb
from xvfbwrapper import Xvfb

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =  config.DB_URI
app.config['SQLALCHEMY_POOL_RECYCLE'] = 3600
app.secret_key = config.secret_key

def conn():
	con = mdb.connect(myconfig.dbhost,
		myconfig.dbuser, myconfig.dbpass, myconfig.dbname)
    
	return con

db.init_app(app)

def check_cookies(t):

	print t.domain

	os.system("killall -9 firefox")

	vdisplay = Xvfb()
	vdisplay.start()
	
	fp = webdriver.FirefoxProfile()
	fp.set_preference("network.proxy.type", 1)
	fp.set_preference("network.proxy.http", 'localhost')
	fp.set_preference("network.proxy.http_port", 8080)
	
	browser = webdriver.Firefox(firefox_profile=fp)
	
	browser.delete_all_cookies()

	t.status = 2
	db.session.commit()
	
	start = datetime.datetime.now()

	try:
		browser.get(t.domain)
	except:
		t.status = 3
		t.info = 'Wrong URL! Task Aborted'
		db.session.commit()

		vdisplay.stop()
		return

	cookies = browser.get_cookies()
	
	end = datetime.datetime.now()

	for co in cookies:
		c = Cookie()
		c.test_id = t.id
		c.name = co['name']
		c.domain = co['domain']
		c.value = co['value'][:200]
		c.expires = co['expiry']

		db.session.add(c)
	
	#ctx = app.test_request_context()
	#ctx.push()
	#proxy_c = ProxyCookie.query.filter(ProxyCookie.datetime.between(start, end))
	#ctx.pop()
	
	con = conn()
	cur = con.cursor(mdb.cursors.DictCursor)
    
	cur.execute("select * from proxy_cookies where datetime between %s and %s", (start,end))
    
	all = cur.fetchall()
	
	for co in all:
		c = Cookie()
		c.test_id = t.id
		c.name = co['name']
		c.domain = co['host']
		c.value = co['value']
		c.expires = co['expiry']
		
		db.session.add(c)

	t.status = 3
	db.session.commit()

	browser.close()
	vdisplay.stop()

if __name__ == '__main__':

    while True:
		ctx = app.test_request_context()
		ctx.push()
		t = Test.query.filter(Test.status==1).first()

		if t:
			try:
				check_cookies(t)
			except Exception,e:
				print str(e)
				t.status = 3
				t.info = "Error! Please try again!"
				
				db.session.commit()
		else:
			sleep(1)

		ctx.pop()

    if browser:
		browser.close()
