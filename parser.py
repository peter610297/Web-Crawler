# -*- coding: UTF-8 -*-
from sgmllib import SGMLParser


##    html parser    ##
##   save data from web page
class htmlparser(SGMLParser):
  
    def reset(self):    
        #using original reset function
        SGMLParser.reset(self)
        #initialization
        self.contentCheck = False                 # 'contentCheck'  for checking main content   <dl>  tag
        self.check_div = False
        self.check_h2 = False
        self.check_dt = False                         # 'check_dt ' for checking  title    <dt> tag
        self.check_dd = False                        # 'check_dd' for  checking  attribute    <dd> tag
        self.tag_attr =  ('class', 'section w570')    # 'tag_attr'  for checking  < dl> 's  attribute
        self.list_type = ""
        self.name = ""
        self.list = {}

    def  resetdata(self): 
        self.list_type =""
        self.name = ""
        self.list = { 1: "",2: "",3: "", 4: "", 5: "", 6: "", 7: ""}

     # checking main content , when read <dl> set  contentCheck =true
    def start_div (self, attrs):
        #check <dl>  with  one attribute
        if len(attrs)  ==1: 
          #compare attribute with  [ class =""datalist ]
          #if true than set contentCheck to true
          if cmp(attrs[0] , self.tag_attr )==0:
              self.check_div=1

    # stop parsing main content when read </dl>
    def end_dl (self):
        self.check_div=False

    def start_h2(self, attrs):
        self.check_h2=1
     
     #stop parsing <dt> tag
    def end_h2(self):
        self.check_h2=False

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
        if self.check_div:

           if self.check_h2: 
                self.name = text

           elif self.check_dt :
                self.list_type = text

           elif   self.check_dd:
                if self.list_type == '工作內容：' :
                      self.list[1] += text 
                elif self.list_type == '工作地點：' :
                      self.list[2] += text 
                elif self.list_type == '工作時間：' :
                      self.list[3] += text 
                elif self.list_type == '工作性質 : ' :
                      self.list[4] += text 
                elif self.list_type == '職務類別：' :
                      self.list[5] += text 
                elif self.list_type == '工作待遇：' :
                      if text != '面議　'  :               
                           text = text.replace(",", "").replace("元", "").replace(" ", "")
                           text =  text[text.index('至')+3:]
                      self.list[6] += text 
                elif self.list_type == '需求人數：' :
                      self.list[7] += text 



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