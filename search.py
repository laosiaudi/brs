#-*- coding:utf-8 -*-
# AUTHOR:   LaoSi
# FILE:     search.py
# 2014 @laosiaudi All rights reserved
# CREATED:  2014-06-05 20:04:49
# MODIFIED: 2014-06-05 21:43:33
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

class SearchHandler(tornado.web.RequestHandler):
    def post(self):
        keyword = self.get_argument("keyword")
        category = self.get_argument("category")

        if category == 'ISBN':
            pass
        elif category == 'bookname':
            pass
        elif category == 'author':
            pass
        

