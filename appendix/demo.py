#encoding=utf-8
# AUTHOR:   LaoSi
# FILE:     demo.py
# 2014 @laosiaudi All rights reserved
# CREATED:  2014-06-05 19:13:12
# MODIFIED: 2014-06-07 20:34:35

import urllib
import time
import sys
import MySQLdb
import re
import json
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')

rfile = open('link.txt','r')
db = MySQLdb.connect(host= "localhost", user= "caijin", passwd= "some_pass", db = "bookdb")
db.set_character_set("utf8")
cur = db.cursor()

data = rfile.readlines()
rfile.close()
TAGS = {
    '0': '小说',
    '1': '随笔',
    '2': '散文',
    '3': '日本文学',
    '4': '童话',
    '5': '诗歌',
    '6': '名著',
    '7': '港台',
    '8': '漫画',
    '9': '绘本',
    '10': '推理',
    '11': '青春',
    '12': '言情',
    '13': '科幻',
    '14': '武侠',
    '15': '奇幻',
    '16': '历史',
    '17': '哲学',
    '18': '传记',
    '19': '设计',
    '20': '建筑',
    '21': '电影',
    '22': '回忆录',
    '23': '音乐',
    '24': '旅行',
    '25': '励志',
    '26': '职场',
    '27': '美食',
    '28': '教育',
    '29': '灵修',
    '30': '健康',
    '31': '家居',
    '32': '经济学',
    '33': '管理',
    '34': '金融',
    '35': '商业',
    '36': '营销',
    '37': '理财',
    '38': '股票',
    '39': '企业史',
    '40': '科普',
    '41': '互联网',
    '42': '编程',
    '43': '交互设计',
    '44': '算法',
    '45': '通信',
    '46': '神经网络'
}

count = 0

for link in data:
    count += 1
    if count % 2 == 0:
        continue

    try:
        pat = re.compile(r'[0-9]+') #设置正则表达式
        
        match = pat.search(link) #匹配搜索
        
        bookid = match.group() #转化成字符串
        
        print "bookid is---------" + bookid
        html = urllib.urlopen("https://api.douban.com/v2/book/" + bookid)
        text = BeautifulSoup(html)
        content = json.loads(text.get_text())
        
        author = content['author'][0].encode("utf-8")
        book_name = content['title'].encode("utf-8")
        pic_url = content['images']['large'].encode("utf-8")
        isbn = content['isbn13'].encode("utf-8")
        publish = content['publisher'].encode("utf-8")
        average_score = float(content['rating']['average'])
        visited = 0
        tags = ""
        for tag in content["tags"]:
            for item in TAGS:
                if (tag['title'] == TAGS[item]):
                    tags += (item + ' ')

        author_intro = content['author_intro'].encode("utf-8")

        print "count is ----------- %d" %(count)
    except:
        time.sleep(3700)


    try:
        cur.execute("INSERT INTO book_info (isbn, book_name, author, publish,\
                picture, visited, average_score, tag, author_intro) VALUES\
                ('%s','%s', '%s', '%s', '%s', '%d', '%f', '%s', '%s')" % (isbn,\
                    book_name, author, publish, pic_url, 0, average_score, tags,\
                    author_intro))
        db.commit()
    except:
        db.rollback()
        print 'failed-----------------------------'

cur.close()
db.close()
