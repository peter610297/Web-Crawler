# -*- coding: UTF-8 -*-

import urllib2
from sgmllib import SGMLParser
import urllib

class htmlparser(SGMLParser):

    def reset(self):
        #using original reset function
        SGMLParser.reset(self)
        #initialization
        self.check_dl= False
        self.check_dd= False
        self.check_li= False
        self.dl_attr = ('id', 'job_result')
        self.a_attr =('class', 'showPositionCss')
        self.urls = []  

    #clear data in the urls
    def  clearURLs(self):
         del self.urls [:]  

     # checking main content , when read <dl> set  contentCheck =true
    def start_dl (self, attrs):
        if len(attrs)  ==2: 
            if cmp(attrs[0] , self.dl_attr ) == 0 :
                 self.check_dl= 1

    def end_dl (self):
        self.check_dl= False

    def start_dd (self, attrs):
        self.check_dd = 1

    def end_dd (self ):
        self.check_dd = False

    def  start_li(self, attrs):
        if  self.check_dl and  self.check_dd :
            if cmp(attrs[0] , self.a_attr ) == 0 :
                 self.check_li =1 

    def end_li (self ):
        self.check_li= False

    def start_a(self, attrs): 
        if self.check_li :
            href = [v for k, v in attrs if k=='href']   
            if href:  
                self.urls.append("http://www.1111.com.tw"+href[0])          
                #print href [0]

    url = 'http://www.1111.com.tw/job-bank/job-index.asp?ss=s&tt=1,2,4,16&d0=160100&si=1&ps=40&trans=1'
for i in range(3):
    print '----------------------------------------------------------'
    print '------------               ' ,i ,'                ------------'
    print '----------------------------------------------------------'
    page = '&page='
    mainpage = url + page + str(i)

'''
#open the given url , and read data to content ( type : string )
url = 'http://www.1111.com.tw/job-bank/job-index.asp?ss=s&tt=1,2,4,16&d0=160100&si=1&ps=40&trans=1'
page = '&page='
a = 1 
mainpage = url + page + str(a)



mainpage = url + page + str(a)
print mainpage


content = urllib2.urlopen(mainpage).read()

#create  SGMLParser object
data = htmlparser()  

###########################

data.feed(content)   #Feed content to parser 
for test in data.urls:
    print test
data.clearURLs()

############################

data.close()


test =  'http://www.1111.com.tw/儲備幹部-台中市-大甲區-找工作-76954510.htm'
print  test

#encode chinese
test1 = urllib.quote(test)
print test1 
'''
#for i in Tempreature.name:
    #if '\t' not in i:
       # print i.decode('utf-8')                

