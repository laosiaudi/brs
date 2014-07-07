#-*- coding:utf-8 -*-
# AUTHOR:   LaoSi
# FILE:     search.py
# 2014 @laosiaudi All rights reserved
# CREATED:  2014-06-05 20:04:49
# MODIFIED: 2014-06-05 22:49:15

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import MySQLdb
import json


db = MySQLdb.connect(host= "localhost", user= "JinnieTsai", passwd= "cj", db
        = "bookdb")
cur = db.cursor()


class SearchHandler(tornado.web.RequestHandler):
    def post(self):
        keyword = self.get_argument("keyword")
        category = self.get_argument("category")

        if category == 'ISBN':
            cur.execute("SELECT * FROM book_info WHERE isbn = %s", keyword)
            book = cur.fetchone()
            self.write(json.dump(book))

        elif category == 'bookname':
            cur.execute("SELECT * FROM book_info WHERE book_name LIKE %%s%", keyword)
            books = cur.fetchall()
            self.write(json.dump(books))

        elif category == 'author':
            cur.execute("SELECT * FROM book_info WHERE author LIKE %%s%", keyword)
            books = cur.fetchall()
            self.write(json.dump(books))
