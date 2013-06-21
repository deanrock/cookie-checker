# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import hashlib
from sqlalchemy.orm import relationship, backref
from sqlalchemy import ForeignKey, Table, Column, Integer, String, Date, Float, DateTime, Text, Boolean
import config
import string,random
import datetime
import urllib

def id_generator(size=6, chars=string.ascii_lowercase + string.digits):
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
    url = db.Column(String(255))
    private = db.Column(Boolean, default = 0)

    def generate_url(self):
        #generate random url

        while True:
            url = id_generator(20)
            
            if Test.query.filter(Test.url == url).count() <= 0:
                break

        self.url = url

    @property
    def serialize(self):
        return {
            #'id': self.id,
            'domain': self.domain,
            'status': self.status,
            'info': self.info,
            'private': self.private,
            'url': self.url,
            'datetime': dump_datetime(self.datetime),
            'finished': dump_datetime(self.finished)
        }

class Url(db.Model):
    __tablename__ = 'urls'

    id = db.Column(Integer, primary_key=True)
    datetime = db.Column(DateTime)
    url = db.Column(String(255))
    test_id = db.Column(Integer, ForeignKey('tests.id'))

    test = relationship('Test', backref=backref('urls'),
            primaryjoin=(Test.id == test_id))

    @property
    def serialize(self):
        return {
                'datetime': self.datetime,
                'url': self.url
               }


class Cookie(db.Model):
    __tablename__ = 'cookies'

    id = db.Column(Integer, primary_key=True)

    url_id = db.Column(Integer, ForeignKey('urls.id'))

    name = db.Column(String(255))
    domain = db.Column(String(255))
    value = db.Column(String(255))
    expires = db.Column(String(255))

    url = relationship('Url', backref=backref('cookies'),
        primaryjoin=(Url.id == url_id))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'domain': self.domain,
            'value': self.value,
            'expires': self.expires
        }

