# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import hashlib
from sqlalchemy.orm import relationship, backref
from sqlalchemy import ForeignKey, Table, Column, Integer, String, Date, Float, DateTime, Text
import config
import string,random
import datetime
import urllib

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

# DB class
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =  config.DB_URI
app.config['SQLALCHEMY_POOL_RECYCLE'] = 3600
app.secret_key = config.secret_key

db = SQLAlchemy(app)

def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]

class Test(db.Model):
	__tablename__ = 'tests'

	id = db.Column(Integer, primary_key=True)
	datetime = db.Column(DateTime)
	domain = db.Column(String(255))
	status = db.Column(Integer)
	info = db.Column(String(255))
	finished = db.Column(DateTime)

	@property
	def serialize(self):
		return {
			'id': self.id,
			'domain': self.domain,
			'status': self.status,
			'info': self.info,
			'datetime': dump_datetime(self.datetime),
			'finished': dump_datetime(self.finished)
		}

class Cookie(db.Model):
	__tablename__ = 'cookies'

	id = db.Column(Integer, primary_key=True)

	test_id = db.Column(Integer, ForeignKey('tests.id'))

	name = db.Column(String(255))
	domain = db.Column(String(255))
	value = db.Column(String(255))

	test = relationship('Test', backref=backref('cookies'), 
		primaryjoin=(Test.id == test_id))

	@property
	def serialize(self):
		return {
			'id': self.id,
			'name': self.name,
			'domain': self.domain,
			'value': self.value,
			'test': self.test_id
		}







