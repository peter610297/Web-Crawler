# -*- coding: UTF-8 -*-

import urllib2
from sgmllib import SGMLParser
 

class htmlparser(SGMLParser):

    contentCheck=False                   # 'contentCheck'  for checking main content   <dl>  tag
    check_dt=False                             # 'check_dt ' for checking  title    <dt> tag
    check_dd=False                            # 'check_dd' for  checking  attribute    <dd> tag
    dl_attr =  ('class', 'dataList')    # 'tag_attr'  for checking  < dl> 's  attribute
    name=[]

     # checking main content , when read <dl> set  contentCheck =true
    def start_dl (self, attrs):
        if len(attrs) == 2:
             print attrs

    def start_a (self, attrs):
         print attrs

#open the given url , and read data to content ( type : string )
content = urllib2.urlopen('http://www.1111.com.tw/job-bank/job-index.asp?ss=s&tt=1,2,4,16&d0=140100&si=1&ps=40&trans=1&page=1').read()

data = htmlparser()  #create  SGMLParser object
data.feed(content)   #Feed content to parser 
data.close()

#for i in Tempreature.name:
    #if '\t' not in i:
       # print i.decode('utf-8')                