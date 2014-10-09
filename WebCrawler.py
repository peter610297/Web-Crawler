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
import sys 

import sql
import parser


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

    url = 'http://www.1111.com.tw/job-bank/job-index.asp?ss=s&tt=1,2,4,16&d0=120100&si=1&ps=40&trans=1' +'&page='
    url_data = parser.URLparser()       # create   URLparser  object


    cate = input('Category : ')
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
     

     
    html = parser.htmlparser()  # create   htmlparser  object
    sql = sql.MS_SQL('140.116.86.51','sa','imilab0936200028*','IMI_db_project')
    urlencode = ""
    urlremove = 0
    progress = ProgressBar( len( url_data.urls ) )


    sql.connect()
    count = 1 
    #get data from web   

    for i in url_data.urls:

        html.resetdata()

        progress.start()

        try:
             urlencode = "http://www.1111.com.tw"+  urllib.quote(i ).replace('%09','%20')
             urlobject   = urllib2.urlopen( urlencode )
             html.feed( urlobject.read() )
        except urllib2.HTTPError:
             urlremove += 1


        # id name content  location time holiday property category salary employee class url
        sql.insert(str(count), html.name,html.list[1],html.list[2],html.list[3],"taiwan",\
                         html.list[4],html.list[5],html.list[6],html.list[7],str(cate), urlencode )
        #sql.insert(str(count),"1","1","1","1","1","1","1","1","1","1","1")
                       
        count+=1

        progress.end()


    # finally print out
    print "not found [",urlremove ,']'
    print "Done ..." 
    html.close()   #clear buffer   
  