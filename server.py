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

db = MySQLdb.connect(host= "localhost", user= "caijin", passwd= "some_pass", db
        = "bookdb", charset= 'utf8')
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
                (r'/settings',SettingHandler),
                (r'/book/(\d+)$',BookHandler),
                (r'/search?',SearchHandler)]
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
            self.write('1') #This indicates that the login successes.
        else:
            self.write('0') #This indicates that the login failed due to the passwd error


class LogoutHandler(BaseHandler):
    def get(self):
        self.set_secure_cookie('user','')
        self.redirect('/login')
class IndexHandler(BaseHandler):
    def get(self):
        cur.execute("SELECT book_name, author, average_score, picture, tag, isbn from \
                book_info order by average_score desc limit 50")
        result = cur.fetchall()
        booklist = []
        for row in result:
            group = {}
            group['bookname'] = row[0]
            group['author'] = row[1]
            group['average_score'] = row[2]
            group['picture'] = row[3]
            group['tag'] = row[4]
            group['isbn'] = row[5]
            group['v'] =  1
            booklist.append(group)
        copy =  booklist[:]
        if self.current_user != '':
            cur.execute("SELECT interests from userinfo_db WHERE email = '%s'" % (self.current_user))
            result= cur.fetchone()
            data = []
            for item in result:
                data.append(item)
            if len(data) != 0:
                titem = data[0].split(',')
                data = titem[:-1]
                for item in data:
                    for book in booklist:
                        taglist = book['tag'].split(' ')[:-1]
                        if not item in taglist:
                            booklist.remove(book)
        #books = json.dumps(booklist)
        newblist =  []
        if len(booklist) < 20:
            for item in booklist:
                for titem in copy:
                    if item['isbn'] == titem['isbn']:
                        newblist.append(item)
                        item['v'] =  0
                        titem['v'] =  0
                        
            for item in booklist:
                if item['v'] ==  1:
                    newblist.append(item)
            for item in copy:
                if item['v'] ==  1:
                    newblist.append(item)
            booklist =  newblist
            print len(booklist)


        self.render("index.html", me=self.current_user,books = booklist)

class BookHandler(BaseHandler):
    def get(self,para):
        print para
        cur.execute("SELECT book_name,author,publish,picture,average_score,tag, author_intro from book_info WHERE \
                isbn = '%s'" % (para))
        row = cur.fetchone()
        group = {}
        group['bookname'] = row[0]
        group['author'] = row[1]
        group['average_score'] = row[4]
        group['picture'] = row[3]
        group['tag'] = row[5]
        group['isbn'] = para
        group['introduction'] =  row[6]
        self.render('book.html',me = self.current_user,book = group)

    def post(self, para):
#        score = self.get_argument('score')
#        isbn = self.get_argument('isbn')
        score =  9.7
        isbn = '9787532740086'
        cur.execute("SELECT user_id from userinfo_db WHERE email = '%s'" %\
                (self.current_user))
        data = cur.fetchone()
        user_id = int(data[0])
        try:
            cur.execute("INSERT INTO score_info (user_id, isbn, score) VALUES ('%d', '%s','%f')" % (user_id, isbn, float(score)))
            print '---'
            db.commit()
            self.write('1')
        except:
            db.rollback()
            self.write('0')

class SearchHandler(tornado.web.RequestHandler):
    def get(self):
        keyword = self.get_argument("kw")
        category = self.get_argument("by")
        print keyword


        if category == 'title':
            cur.execute("SELECT * FROM book_info WHERE book_name LIKE '%s' " %
                    ('%' + keyword + '%'))
            books = cur.fetchall()
            booklist = []
            for row in books:
                group = {}
                group['bookname'] = row[1]
                group['author'] = row[2]
                group['publish'] = row[3]
                group['average_score'] = row[6]
                group['picture'] = row[4]
                group['tag'] = row[7]
                group['isbn'] = row[0]
                booklist.append(group)
            self.render('index.html',me=self.current_user,books=booklist)

        elif category == 'author':
            cur.execute("SELECT * FROM book_info WHERE author LIKE '%s' " % ('%'
                + keyword + '%'))
            books = cur.fetchall()
            booklist = []
            for row in books:
                group = {}
                group['bookname'] = row[1]
                group['author'] = row[2]
                group['publish'] = row[3]
                group['average_score'] = row[6]
                group['picture'] = row[4]
                group['tag'] = row[7]
                group['isbn'] = row[0]
                booklist.append(group)
            self.render('index.html',me=self.current_user,books=booklist)                
        
        


class SettingHandler(BaseHandler):
    def get(self):
        if self.current_user != '':
            cur.execute("SELECT interests from userinfo_db WHERE email = '%s'" % (self.current_user))
            result= cur.fetchone()
            data = []
            for item in result:
                titem = item.split(',')
                for digit in titem:
                    data.append(digit)
            self.render("settings.html",me=self.current_user, tags = data[:-1])
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
            self.write('1')


if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()



