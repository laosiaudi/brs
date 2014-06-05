#-*-coding:utf-8-*-
import MySQLdb
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default = 8000, help = "run on the given port", type = int)

db = MySQLdb.connect(host= "localhost", user= "JinnieTsai", passwd= "cj", db
        = "bookdb")
cur = db.cursor()

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("base.html")


class RegisterHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("register.html")

    def post(self):
        Email = self.get_argument("exampleInputEmail2")
        Username = self.get_argument("username")
        Password = self.get_argument("pw1")
        Interests = self.get_argument("interests")
        same_email =  cur.execute("SELECT * FROM userinfo_db WHERE email = %s
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
    app = tornado.web.Application(handlers=[(r"/base", IndexHandler),
        (r"/register", RegisterHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()




