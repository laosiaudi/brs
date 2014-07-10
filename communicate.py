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
from basic import *
from user import *
class DiscussHandler(BaseHandler):
    def get(self):
        groupset = self.application.group
        self.render('discuss.html', me = self.current_user, groups =
                list(groupset.find()))
    def post(self):
        groupname = self.get_argument("groupname")
        groupintro = self.get_argument("groupintro")
        if self.application.group.find_one({'name':groupname}) != None:
            self.write("0")
            return
        upload_path = os.path.join(os.path.dirname(__file__), 'files')
        '''if self.request.files.get('uploadpic', None):
            uploadFile = self.request.files['uploadpic'][0]
            filename = groupname
            filepath = os.path.join(upload_path,filename)
            with open(filepath, 'wb+') as up:
                up.write(uploadFile['body'])
            newGroupSet = {}
            newGroupSet['name'] = groupname.encode('utf-8')
            newGroupSet['intro'] = groupintro.encode('utf-8')
            self.application.group.insert(newGroupSet) 
            self.write("1")
        else:
            print '-----------*----------xxxxxxx'
            self.write("0")
        '''
        newGroupSet = {}
        newGroupSet['name'] = groupname.encode('utf-8')
        newGroupSet['intro'] = groupintro.encode('utf-8')
        newGroupSet['admin'] = self.current_user
        self.application.group.insert(newGroupSet) 
        self.write("1")
class GroupHandler(BaseHandler):
    def get(self, para):
        self.write("To be Continued.....")


