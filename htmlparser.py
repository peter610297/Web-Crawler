# -*- coding: UTF-8 -*-

'''
2014  database 
using SGMLParser html parsering  tool
-----------------------
截取1111人力銀行網頁資訊, 從< div class="datalist"></div>中抓取工作資訊
-----------------------
'''

import urllib2
from sgmllib import SGMLParser
 

class htmlparser(SGMLParser):

    contentCheck=False                   # 'contentCheck'  for checking main content   <dl>  tag
    check_dt=False                             # 'check_dt ' for checking  title    <dt> tag
    check_dd=False                            # 'check_dd' for  checking  attribute    <dd> tag
    tag_attr =  ('class', 'dataList')    # 'tag_attr'  for checking  < dl> 's  attribute

    name=[]

     # checking main content , when read <dl> set  contentCheck =true
    def start_dl (self, attrs):
        #check <dl>  with  one attribute
        if len(attrs)  ==1: 
          #compare attribute with  [ class =""datalist ]
          #if true than set contentCheck to true
          if cmp(attrs[0] , self.tag_attr )==0:
              self.contentCheck=1

    # stop parsering main content when read </dl>
    def end_dl (self):
        self.contentCheck=False

     # checking title , when read <dt> tag  set check_dt = true  
    def start_dt(self, attrs):
        self.check_dt=1
     
     #stop parsering <dt> tag
    def end_dt(self):
        self.check_dt=False

     # checking attribute  ,  when read <dd> tag set check_dd  = true
    def start_dd(self, attrs):
        self.check_dd=1

    #stop parsering <dd> tag
    #print newline when </dd>  is in main content
    def end_dd (self):
        if self.contentCheck:
             print  "\n"  
        self.check_dd=False

    #get the data  between <dt> and  </dt>  for  title
    #                                            <dd> and </dd>  for  contents
    def handle_data(self, text):  
        if self.contentCheck:
          if self.check_dt:
               print  text,  #  ',' will not print newline 
          elif   self.check_dd:
               print  text,  #  ',' will not print newline

#open the given url , and read data to content ( type : string )
content = urllib2.urlopen('http://www.1111.com.tw/%E6%B6%88%E9%98%B2%E8%A8%AD%E5%82%99%E5%A3%AB-%E5%8F%B0%E4%B8%AD%E5%B8%82-%E5%8C%97%E5%B1%AF%E5%8D%80-%E6%89%BE%E5%B7%A5%E4%BD%9C-77058600.htm').read()

data = htmlparser()  #create  SGMLParser object
data.feed(content)   #Feed content to parser 
data.close()

#for i in Tempreature.name:
    #if '\t' not in i:
       # print i.decode('utf-8')                