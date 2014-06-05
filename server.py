#-*-coding:utf-8-*-
import MySQLdb
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os
from tornado.options import define, options
define("port", default = 8000, help = "run on the given port", type = int)

db = MySQLdb.connect(host= "localhost", user= "root", passwd= "123456", db
        = "bookdb")
cur = db.cursor()

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r'/base',IndexHandler),
                (r'/register',RegisterHandler),
                (r'/login',LoginHandler)]
        settings = dict(template_path=os.path.join(os.path.dirname(__file__), "templates"),
                static_path=os.path.join(os.path.dirname(__file__), "static"),
                cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
                debug=True,)
        tornado.web.Application.__init__(self, handlers, **settings)

class LoginHandler(BaseHandler):
    def get(self):
        if self.current_user != '':
            self.redirect('/base')
        else:
            self.render("login.html", me=self.current_user)

    def post(self):
        usr = self.get_argument('email','')
        password = self.get_argument('pass','')
        record = cur.execute("SELECT * FROM userinfo_db WHERE email = %s\
                and user_name = %s", (usr,password))
        if cur.rowcount > 0:
            self.set_secure_cookie("user",email)
            self.redirect('/base')
        else:
            self.write('0')

class IndexHandler(BaseHandler):
    def get(self):
       self.render("base.html", me=self.current_user)



class RegisterHandler(BaseHandler):
    def get(self):
        self.render("register.html", me=self.current_user)

    def post(self):
        Email = self.get_argument("exampleInputEmail2")
        Username = self.get_argument("username")
        Password = self.get_argument("pw1")
        Interests = self.get_argument("interests")
        same_email =  cur.execute("SELECT * FROM userinfo_db WHERE email = %s\
                or user_name = %s", (Email, Username))
        if cur.rowcount > 0:
            '''This indicates that some user has already existed with the same
            email or the same user name'''
            self.write("1")
        else:
            total_user = cur.execute("SELECT * FROM userinfo_db")
            user_id = cur.rowcount + 1
            cur.execute("INSERT INTO userinfo_db (email, user_name, user_id,passwd, interests) VALUES (%s, %s, %d, %s, %s)", (Email,
                        Username, user_id, Password, Interests))
            db.commit()
            '''This indicates that this user register successfully'''
            self.write("0")


if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()



