#-*-coding:utf-8-*-
import MySQLdb
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os
import md5
from tornado.options import define, options
import json
define("port", default = 8000, help = "run on the given port", type = int)

db = MySQLdb.connect(host= "localhost", user= "root", passwd= "123456", db
        = "bookdb")
db.set_character_set('utf8')
cur = db.cursor()

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r'/',IndexHandler),
                (r'/register',RegisterHandler),
                (r'/login',LoginHandler),
                (r'/logout',LogoutHandler),
                (r'/settings',SettingHandler)]
        settings = dict(template_path=os.path.join(os.path.dirname(__file__), "templates"),
                static_path=os.path.join(os.path.dirname(__file__), "static"),
                cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
                debug=True,)
        tornado.web.Application.__init__(self, handlers, **settings)

class LoginHandler(BaseHandler):
    def get(self):
        if self.current_user != '':
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
            self.redirect('/')
        else:
            self.write('0') #This indicates that the login failed due to the passwd error


class LogoutHandler(BaseHandler):
    def get(self):
        self.set_secure_cookie('user','')
        self.redirect('/login')
class IndexHandler(BaseHandler):
    def get(self):
        cur.execute("SELECT book_name, author, average_score, picture from \
                book_info order by average_score desc limit 20")
        result = cur.fetchall()
        booklist = []
        for row in result:
            group = {}
            group['bookname'] = row[0]
            group['author'] = row[1]
            group['average_score'] = row[2]
            group['picture'] = row[3]
            print group['bookname']
            booklist.append(group)
        if self.current_user != '':
            pass
        #books = json.dumps(booklist)
        self.render("index.html", me=self.current_user,books = booklist)


class SettingHandler(BaseHandler):
    def get(self):
        if self.current_user != '':
            self.render("settings.html",me=self.current_user)
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
            self.redirect('/')
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
        same_email =  cur.execute("SELECT * FROM userinfo_db WHERE email = %s", (Email))
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
            self.redirect('/login')


if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()



