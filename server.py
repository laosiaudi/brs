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
import pymongo
from basic import *
from user import *
from communicate import *
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r'/',IndexHandler),
                (r'/register',RegisterHandler),
                (r'/login',LoginHandler),
                (r'/logout',LogoutHandler),
                (r'/settings',SettingHandler),
                (r'/book/(\d+)$',BookHandler),
                (r'/search?',SearchHandler),
                (r'/discuss',DiscussHandler),
                (r'/group/(.*)',GroupHandler)]
        settings = dict(template_path=os.path.join(os.path.dirname(__file__), "templates"),
                static_path=os.path.join(os.path.dirname(__file__), "static"),
                cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
                debug=True,)

        conn=pymongo.Connection("localhost",27017)
        commentDB=conn["commentDB"]
        self.db = conn.commentDB.commentSet
        self.group = conn.commentDB.groupSet
        tornado.web.Application.__init__(self, handlers, **settings)
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
        if self.current_user != '' and self.current_user !=  None:
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
        commentset = self.application.db
        commentinfo = commentset.find_one({"isbn":para})
        newcom = []
            
        if commentinfo == None:
            self.render('book.html',me = self.current_user,book = group, comments='')
        else:
            com = commentinfo['comment']
            for item in com:
                cur.execute("SELECT email from userinfo_db WHERE user_id = '%d'" %\
                        (int(item)))
                data = cur.fetchone()
                email  =  data[0]
                percom = {'user': email, 'text': com[item]}
                newcom.append(percom)
            self.render('book.html',me = self.current_user,book = group,
                    comments=newcom)


    def post(self, para):
        score = self.get_argument('scoreRange')
        comment = self.get_argument('comment')
        #isbn = self.get_argument('isbn')
        isbn =  para
        cur.execute("SELECT user_id from userinfo_db WHERE email = '%s'" %\
                (self.current_user))
        data = cur.fetchone()
        user_id = int(data[0])
        try:
            cur.execute("REPLACE INTO score_info (user_id, isbn, score) VALUES ('%d', '%s','%f')" % (user_id, isbn, float(score)))
            db.commit()
        except:
            db.rollback()
            self.write('0')
        commentSet = self.application.db
        bookset = commentSet.find_one({"isbn":isbn})
        if bookset == None:
            newset = {}
            newset['isbn'] = isbn
            commentpair = {}
            commentpair[str(user_id).encode('utf-8')] = comment
            newset['comment'] = commentpair
            self.application.db.insert(newset)

        else:
            bookset['comment'][str(user_id).encode('utf-8')] = comment
            self.application.db.update({"isbn":isbn},{"$set":bookset})
        self.write('1')


class SearchHandler(tornado.web.RequestHandler):
    def get(self):
        keyword = self.get_argument("kw")
        category = self.get_argument("by")

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
            self.render('search.html',me=self.current_user,books=booklist)

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
            self.render('search.html',me=self.current_user,books=booklist)                
        

if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()



