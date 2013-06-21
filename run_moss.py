url = 'http://www.moss-soz.si/si/rezultati_moss/obdobje/default.html'

import re
import urllib, urllib2
import requests
import json

f = urllib.urlopen(url)
content = f.read()

def test_url(url):
	payload = {'public':'yes',
		'domain':url}
	print "a"
	data = payload
	print "b"
	r = requests.post('http://cookies.kirrupt.com/check', 
		data=data)
	print "x"

x = re.findall('<strong>(.*)<\/strong>', content)

y = x[:-1]

i = 0
test
for x in y:
	x = x.split('<')

	i = i+1
	print "%d. %s" % (i, x[0])
	test_url(x[0])
