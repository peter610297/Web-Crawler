# -*- coding: UTF-8 -*-
from sgmllib import SGMLParser


'''---------------company parser ---------------                            
         Get data from company page
-----------------------------------------------'''
class comparser(SGMLParser):
  
    def reset(self):    
        SGMLParser.reset(self)
        self.name = ""
        self.site = ""
        self.address = ""

        self.dl_attr = ('class', 'dataList')           # use for searching  <dl> tag  with "id = job_result" 
        self.attr = ""
        self.check_dl = False
        self.check_dt = False
        self.check_dd = False

     # when read <dl> set  contentCheck =true
    def start_dl (self, attrs):
        # read <dl> tag with 2 attributes
        if len(attrs)  == 1: 
             # set check_dl when <dl>  attribute equal to ('class', 'dataList')
            if cmp(attrs[0] , self.dl_attr ) == 0 :
                 self.check_dl= 1

    #stop parsing <dl> tag 
    def end_dl (self):
        self.check_dl= False

    def start_dt (self, attrs):
        if self.check_dl:
            self.check_dt = 1

    # stop parsing <dd> tag
    def end_dt (self ):
        self.check_dt = False

    def start_dd (self, attrs):
        if self.check_dl:
            self.check_dd = 1

    # stop parsing <dd> tag
    def end_dd (self ):
        self.check_dd = False

    #Reading content in <div> get the data  between
    # <h2> and  </h2>  for  title & <dd> and </dd>  for  contents 
    def handle_data(self, text): 
        if self.check_dl:  
            if self.check_dt:
                self.attr = text 
            elif self.check_dd :
                text = text.replace(",", "").replace(" ", "")
                if self.attr == '公司名稱：' and text != "商業登記" :
                    self.name = text
                elif self.attr == '聯絡地址：' and text != "" :
                    self.address  = text 
                elif self.attr == '網站位址：' and text != "" :
                    self.site = text




'''---------------html parser ---------------                            
          Get data from web page
-----------------------------------------------'''
class htmlparser(SGMLParser):
  
    def reset(self):    
        #using original reset function
        SGMLParser.reset(self)
        #initialization
        self.check_div = False           # 'check_div ' for checking  title <div> tag
        self.check_h2 = False            # 'check_h2 ' for checking  title <h2> tag
        self.check_dt = False             # 'check_dt ' for checking  title <dt> tag
        self.check_dd = False            # 'check_dd' for  checking  attribute  <dd> tag
        self.check_a = False 
        self.check_ul = False 

        self.tag_attr1 =  ('class', 'section w570')    # 'tag_attr'  for checking  < dl> 's  attribute
        self.tag_attr2 =  ('class', 'navbar')
        self.list_type = ""    #Decide which  table attribute is reading 
        self.name = ""        #Job title
        self.list = {}            #Save data of all attribute (type : dict)
        self.tempcomurl = ""
        self.comurl = ""

    def  resetdata(self): 
        self.list_type =""
        self.name = ""
        self.list = { 1: "",2: "",3: "", 4: "", 5: "", 6: "", 7: ""}
        self.tempcomurl = ""

     # checking main content , when read <div> set  check_div =true
    def start_div (self, attrs):
        #check <div>  with  one attribute
        if len(attrs)  ==1: 
          #compare attribute with  [ class ="section w570" ]
          #if true than set check_div to true
          if cmp(attrs[0] , self.tag_attr1 )==0:
              self.check_div=1

    # stop parsing main content when read </div>
    def end_div (self):
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

    # For getting company information page

    def start_ul(self, attrs):
      if len(attrs)  ==1: 
          if cmp(attrs[0] , self.tag_attr2 )==0:
              self.check_ul = 1

    def end_ul(self):
        self.check_ul = False

    def start_a(self, attrs):
        if self.check_ul: 
            self.tempcomurl = [v for k, v in attrs if k=='href'] 
            self.check_a = 1

    def end_a(self):
        self.check_a = False

    #Reading content in <div> get the data  between
    # <h2> and  </h2>  for  title & <dd> and </dd>  for  contents 
    def handle_data(self, text):  

        if self.check_div:
           #Get job titile 
           if self.check_h2: 
                self.name = text
             
           #Get type of attribute  
           elif self.check_dt :
                self.list_type = text
           #Save data to corresponding attribute
           elif   self.check_dd:
                if self.list_type == '工作內容：' :  #content
                      #Trim ' , ' in the string
                      text = text.replace(",", "")  
                      self.list[1] += text 
                elif self.list_type == '工作地點：' : #location
                      self.list[2] += text 
                elif self.list_type == '工作時間：' : #time
                      self.list[3] += text 
                elif self.list_type == '工作性質：' : #property
                      self.list[4] += text 
                elif self.list_type == '職務類別：' : #catogory
                      self.list[5] += text 
                elif self.list_type == '需求人數：' : #people require
                      self.list[7] += text
                elif self.list_type == '工作待遇：' : # salary
                       #There two type in salary  面議 & salary
                       #and we will get the max salary if its not 面議
                      if text != '面議　'  :     
                           #Trim ' , '  & ' 元 '  & /space in the string 
                           text = text.replace(",", "").replace("元", "").replace(" ", "")
                           #Get the number in the string           
                           if "至" in text :
                               text =  text[ text.index('至')+3 : ]
                           else:
                               text =  text[ text.index('薪')+3 : ]
                      #Save result         
                      self.list[6] += text 

        elif  self.check_a: 
            if text == "公司基本資料": 
                self.comurl = self.tempcomurl[0]


'''---------------URL  parser ---------------                            
       Get all links from web page
---------------------------------------------------'''
class URLparser(SGMLParser):

    def reset(self):
        #using original reset function
        SGMLParser.reset(self)
        #initialization
        self.check_dl= False    # checking <dl> tag 
        self.check_dd= False    #  checking <dd> tag
        self.check_li= False    #  checking <li> tag
        self.urls = []          #Store all url 

        self.dl_attr = ('id', 'job_result')           # use for searching  <dl> tag  with "id = job_result" 
        self.a_attr =('class', 'showPositionCss')     # use for searching  <a> tag with "id = showPositionCss"         

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