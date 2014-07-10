import MySQLdb
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os
import md5
from tornado.options import define, options
import json
import pymongo


define("port", default = 8000, help = "run on the given port", type = int)

db = MySQLdb.connect(host= "localhost", user= "root", passwd= "123456", db
        = "bookdb", charset= 'utf8')
db.set_character_set('utf8')
cur = db.cursor()


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")


