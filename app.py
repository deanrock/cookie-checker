# -*- coding: utf-8 -*-

from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, make_response, jsonify, Response
import json, datetime
from datetime import timedelta
from time import mktime
from functools import wraps
from urllib import urlopen
import urllib
import string,random
from flask import Flask
import hashlib
import string,random
import datetime
import urllib
import hashlib
import string,random
from model import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =  config.DB_URI
app.config['SQLALCHEMY_POOL_RECYCLE'] = 3600
app.secret_key = config.secret_key

db.init_app(app)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/test/<id>')
def test(id):
	test = Test.query.get(id)

	return render_template('test.html', test=test)

@app.route('/js-test-info/<id>')
def js_test_info(id):
	test = Test.query.get(id)

	return jsonify({'test':test.serialize})

@app.route('/js-get-cookies/<id>')
def js_get_cookies(id):
	test = Test.query.get(id)

	cookies = [c.serialize for c in test.cookies]

	cookies_distinct = []

	for c in cookies:
		found = False

		for co in cookies_distinct:
			if co['domain'] == c['domain'] and co['name'] == c['name']:
				found = True
				break

		if not found:
			cookies_distinct.append(c)
            
	return jsonify({'cookies': cookies_distinct})

@app.route('/check', methods=['POST'])
def check():
	if 'domain' in request.form:
		domain = request.form['domain']

		test = Test()
		test.domain = domain
		test.datetime = datetime.datetime.now()
		test.status = 1

		db.session.add(test)
		db.session.commit()

		return redirect(url_for('test', id=test.id))

	return redirect(url_for('index'))

@app.route('/history')
def history():
	return render_template('history.html', tests = Test.query.order_by(Test.id.desc()).all())

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=2000)
