#-*- coding:utf-8 -*-
# AUTHOR:   LaoSi
# FILE:     demo.py
# 2014 @laosiaudi All rights reserved
# CREATED:  2014-06-05 19:13:12
# MODIFIED: 2014-06-05 19:39:08

import urllib
import re
import json
from bs4 import BeautifulSoup
rfile = open('link.txt','r')

data = rfile.readlines()

link = data[0]
pat = re.compile(r'[0-9]+') #设置正则表达式

match = pat.search(link) #匹配搜索

bookid = match.group() #转化成字符串
rfile.close()

html = urllib.urlopen("https://api.douban.com/v2/book/" + bookid)
text = BeautifulSoup(html)
print text.get_text()
content = json.loads(text.get_text())

print content['author'][0].encode('utf-8')
print content['title'].encode('utf-8')
print content['images']

small_pic = content['images']['small']
medium_pic = content['images']['medium']
big_pic = content['images']['large']

urllib.urlretrieve(small_pic,bookid+'_small.jpg')
urllib.urlretrieve(medium_pic,bookid+'_medium.jpg')
urllib.urlretrieve(big_pic,bookid+'_big.jpg')


