# -*- coding: UTF-8 -*-

'''
2014  database 
using SGMLParser html parseing  tool
-----------------------
截取1111人力銀行網頁資訊, 從< div class="datalist"></div>中抓取工作資訊
-----------------------
'''
from __future__ import division
from sgmllib import SGMLParser
import urllib
import urllib2
import sql
import sys 


##    html parser    ##
##   save data from web page
class htmlparser(SGMLParser):
  
    def reset(self):    
        #using original reset function
        SGMLParser.reset(self)
        #initialization
        self.contentCheck=False                 # 'contentCheck'  for checking main content   <dl>  tag
        self.check_dt=False                         # 'check_dt ' for checking  title    <dt> tag
        self.check_dd=False                        # 'check_dd' for  checking  attribute    <dd> tag
        self.tag_attr =  ('class', 'dataList')    # 'tag_attr'  for checking  < dl> 's  attribute
        self.data = []  

     # checking main content , when read <dl> set  contentCheck =true
    def start_dl (self, attrs):
        #check <dl>  with  one attribute
        if len(attrs)  ==1: 
          #compare attribute with  [ class =""datalist ]
          #if true than set contentCheck to true
          if cmp(attrs[0] , self.tag_attr )==0:
              self.contentCheck=1

    # stop parsing main content when read </dl>
    def end_dl (self):
        self.contentCheck=False

     # checking title , when read <dt> tag  set check_dt = true  
    def start_dt(self, attrs):
        self.check_dt=1
     
     #stop parsing <dt> tag
    def end_dt(self):
        self.check_dt=False

     # checking attribute  ,  when read <dd> tag set check_dd  = true
    def start_dd(self, attrs):
        self.check_dd=1

    #stop parsing <dd> tag
    def end_dd (self):
        #print newline when </dd>  is in main content
        #if self.contentCheck:
             #print  "\n"  
        self.check_dd=False

    #get the data  between <dt> and  </dt>  for  title
    #                                     <dd> and </dd>  for  contents
    
    def handle_data(self, text):  
        if self.contentCheck:
          #if self.check_dt:
                 #text,  #  ',' will not print newline  
          if   self.check_dd:
               self.data.append(text)  #  ',' will not print newline

    def  cleardata(self):
         del self.data [:] 

##   html parser ##
##   save data from web page
class URLparser(SGMLParser):

    def reset(self):
        #using original reset function
        SGMLParser.reset(self)
        #initialization
        self.check_dl= False               # checking <dl> tag 
        self.check_dd= False              #  checking <dd> tag
        self.check_li= False                #  checking <li> tag
        self.dl_attr = ('id', 'job_result')                   # use for searching  <dl> tag  with "id = job_result" 
        self.a_attr =('class', 'showPositionCss')     # use for searching  <a> tag with "id = showPositionCss"
        self.urls = []  

    # clear all data in the urls
    def  clearURLs(self):
         del self.urls [:]  

     # when read <dl> set  contentCheck =true
    def start_dl (self, attrs):
        # read <dl> tag with 2 attributes
        if len(attrs)  ==2: 
             # set check_dl when <dl>  attribute equal to ('id', 'job_result')
            if cmp(attrs[0] , self.dl_attr ) == 0 :
                 self.check_dl= 1

    #stop parsing <dl> tag 
    def end_dl (self):
        self.check_dl= False
     
     # start parsing <dd> tag
    def start_dd (self, attrs):
        self.check_dd = 1

    # stop parsing <dd> tag
    def end_dd (self ):
        self.check_dd = False

    # start parsing <li > tag 
    def  start_li(self, attrs):
        #read <li>  when <li>  is in the right  <dl> & <dd>
        if  self.check_dl and  self.check_dd :
             #compare <a> 's  attribute with  ('class', 'showPositionCss') 
             # then set check_li = true
            if cmp(attrs[0] , self.a_attr ) == 0 :
                 self.check_li =1 

     #stop parsing  <li> tag 
    def end_li (self ):
        self.check_li= False
     
     # start parsing <a> tag 
    def start_a(self, attrs):
        # get  web url in the <a>   tag  
        if self.check_li :
            href = [v for k, v in attrs if k=='href'] 
            # save  url  in the  urls list 
            if href:  
                self.urls.append( href[0] )          

class ProgressBar():
    def __init__(self, lenth=100):
        self.pointer = 0
        self.width = 50
        self.range = lenth -1
        self.count = 0

    def start(self):
         self.pointer = int(self.width*(self.count /self.range))
         sys.stdout.write("|" + ">"*self.pointer + "-"*(self.width-self.pointer)+"|"+str(int((self.count /self.range)*100))+'%  ['+str(self.count +1)+'/'+str(self.range+1)+'] '+"\r")
         sys.stdout.flush()
         self.count +=1

    def end(self):
         if self.count == self.range+1: 
              print


if __name__ == "__main__":

    url = 'http://www.1111.com.tw/job-bank/job-index.asp?ss=s&tt=1,2,4,16&d0=100100&si=1&ps=40&trans=1' +'&page='
    url_data = URLparser()       # create   URLparser  object
    pagenum = input('Pages：')

    #  parsing each page 
    for  page in range(1, pagenum+1):
        mainpage = url + str(page)
        #create  SGMLParser object
        url_data.feed( urllib2.urlopen(mainpage).read() )   #Feed content to parser 

        sys.stdout.write('catching urls ... ['+str( len(url_data.urls) )+"]\r")
        sys.stdout.flush()

    url_data.close()       #clear buffer    
     
    print "\nstart parsing websites ..."
     
    html = htmlparser()  # create   htmlparser  object
    sql = sql.MS_SQL('140.116.86.51','sa','imilab0936200028*','IMI_db_project')
    urlencode = ""
    urlremove = 0
    progress = ProgressBar( len( url_data.urls ) )

    sql.connect()

    #get data from web   
    for i in url_data.urls:

        progress.start()

        try:
             urlencode = "http://www.1111.com.tw"+  urllib.quote(i ).replace('%09','%20')
             urlobject   = urllib2.urlopen( urlencode )
             html.feed( urlobject.read() )
        except urllib2.HTTPError:
             urlremove += 1

        sql.insert( html.data[0] ) 

        html.cleardata()

        progress.end()

    # finally print out
    print "not found [",urlremove ,']'
    print "Done ..." 
    html.close()   #clear buffer   
  