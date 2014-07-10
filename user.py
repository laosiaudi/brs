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
class LoginHandler(BaseHandler):
    def get(self):
        if self.current_user != '' and self.current_user !=  None:
            self.redirect('/')
        else:
            self.render("login.html", me=self.current_user)

    def post(self):
        usr = self.get_argument('email','')
        password = self.get_argument('pw1','')
        key = md5.new()
        key.update(password)
        record = cur.execute("SELECT * FROM userinfo_db WHERE email = %s and passwd = %s", (usr,key.hexdigest()))
        if cur.rowcount > 0:
            self.set_secure_cookie("user",usr)
            self.write('1') #This indicates that the login successes.
        else:
            self.write('0') #This indicates that the login failed due to the passwd error


class LogoutHandler(BaseHandler):
    def get(self):
        self.set_secure_cookie('user','')
        self.redirect('/login')


class SettingHandler(BaseHandler):
    def get(self):
        if self.current_user != '' and self.current_user !=  None:
            cur.execute("SELECT interests from userinfo_db WHERE email = '%s'" % (self.current_user))
            result= cur.fetchone()
            data = []
            for item in result:
                titem = item.split(',')
                for digit in titem[:-1]:
                    data.append(int(digit))
            print data
            self.render("settings.html",me=self.current_user, tags = data)
        else:
            self.redirect('/login')

    def post(self):
        pw1 = self.get_argument('pw1')
        pw2 = self.get_argument('pw2')
        Interests = ''
        for i in range(47):
            if self.get_argument(str(i),None) !=None:
                Interests += str(i) + ','
        key = md5.new()
        key.update(pw1)
        newkey = md5.new()
        newkey.update(pw2)
        try:
            cur.execute("UPDATE userinfo_db SET passwd = '%s' , interests = '%s' WHERE email = '%s' and passwd = '%s'" % \
                    (newkey.hexdigest(),Interests ,self.current_user,key.hexdigest()))
            db.commit()
            self.write('1')
        except:
            db.rollback()
            self.write('0') #This indicates that the settings update failed


class RegisterHandler(BaseHandler):
    def get(self):
        if self.current_user == '' or self.current_user == None:
            self.render("register.html", me=self.current_user)
        else:
            self.redirect('/')

    def post(self):
        Email = self.get_argument("email")
        Password = self.get_argument("pw1")
        key = md5.new()
        key.update(Password);
        Interests = ''

        for i in range(47):
            if self.get_argument(str(i),None) !=None:
                Interests += str(i) + ','
        same_email =  cur.execute("SELECT * FROM userinfo_db WHERE email = '{0}'".format(Email))
        if cur.rowcount > 0:
            '''This indicates that some user has already existed with the same
            email or the same user name'''
            self.write("0") #This indicates that the register failed due to duplicated username
        else:
            total_user = cur.execute("SELECT * FROM userinfo_db")
            user_id = cur.rowcount + 1
            user_id = int(user_id)
            store_pass = key.hexdigest()
            cur.execute("INSERT INTO userinfo_db (passwd,email,user_id, interests) VALUES ('%s', '%s',\
                   '%d','%s')" % (store_pass, Email,user_id,Interests))
            db.commit()
            '''This indicates that this user register successfully'''
            self.write('1')
