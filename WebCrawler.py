# -*- coding: UTF-8 -*-
from __future__ import division
import urllib
import urllib2
import sys 
import os
import time
import datetime
import sql        
import parser


class ProgressBar():

    def __init__(self, lenth):
        self.pointer = 0            # '>' 's  length
        self.width = 50             #Width of progress bar
        self.range = lenth -1   #Number of total URLs
        self.count = 0              #Number of read URLs

    def start(self): 
         #Calculate lenth of pointer
         self.pointer = int(self.width*(self.count /self.range))

         #Print progress bar & progress percentage & number of  pages read
         sys.stdout.write("|" + ">"*self.pointer + "-"*(self.width-self.pointer)+"|"+str(int((self.count /self.range)*100))+'% ('+str(self.count +1)+' pages) '+"\r")
         sys.stdout.flush()
         self.count +=1



if __name__ == "__main__":

    
    #Print all Categories of the job
    print "--- [Category] ---"
    print "(1)生產製程(2)光電半導體(3)軟體工程"
    print "(4)電腦硬體(5)系統規劃(6)網路管理"

    #Get input of Job Category type & main URL  & number of pages to read 
    cate = input('---Select a category: ')
    mainURL = raw_input("---URL : ") 
    pagenum = input('---How many Pages：')
    location = raw_input('---Location(n/e/s/w) : ')


    #Use dict type to decide which categiry type was selected
    category= { 1: "生產製程",2: "光電半導體",3: "軟體工程", 4: "電腦硬體", \
                5: "系統規劃", 6: "網路管理"}
    
    #Create  URLparser object
    url_data = parser.URLparser()       


    '''
    ''Get all the link  in each pages
    ''
    '''
    for  page in range(1, pagenum+1):
        #www.1111.com  pages is controled by  &page= <num>
        #so can <num> we can read each page from main page
        mainpage = mainURL + '&page=' + str(page)

        #Feed content to parser , get the link's url in <dl id="job_result"> tag 
        url_data.feed( urllib2.urlopen(mainpage).read() )  

        #Print total number of URLs
        sys.stdout.write('catching urls ... ['+str( len(url_data.urls) )+"]\r")
        sys.stdout.flush()  #Flush the buffer



    #Create MS_SQL object , information of database
    sql = sql.MS_SQL('140.116.86.51','sa',"imilab0936200028*",'IMI_db_project')

    #Connect to the MS SQL server
    sql.connect()


    #Create  htmlparser object
    job = parser.jobparser() 
    com = parser.comparser()

    #Create  ProgressBar object , print process during parsing webpage  
    progress = ProgressBar( len( url_data.urls ) )



    urlencode = ""     #Save encoded URL
    urlremove = 0      #Record number of missing pages
    id_count = sql.getID()       #Represent key value in the database table 
    URLnum =  len(url_data.urls)  #get total url  quantity



    #Print information of start parsing process
    print "\nstart parsing websites ..."



    '''
    ''Parsing all webpage we got
    ''
    '''
    for i in url_data.urls:         
        #Reset data in the htmlparser while starting parsing new page
        job.resetdata()
         
        #Print progress bar in the screen
        progress.start()

        #Use try & exception to avoid feeding missing webpage
        #to  htmlparser , record missing webpage by urlremove
        try:
             #Because /tab in the http will lead to error
             #so replace UTF-8 code /tab (=%09) to /space (=%20)
             urlencode = "http://www.1111.com.tw"+  urllib.quote(i ).replace('%09','%20')

             job.feed( urllib2.urlopen(urlencode).read() )

             #get company information
             com_url   = "http://www.1111.com.tw"+ urllib.quote(job.comurl ).replace('%09','%20')
             com.feed( urllib2.urlopen( com_url ).read() )



        except urllib2.HTTPError:
             #Plus 1 to urlremove if http 404 not found
             urlremove += 1



        '''
        ''Insert data inte database 
        ''
        '''

        #(self, id, name, c, cla, time, sal, h, req, addr, loc, corpName):
        #Save date into the JOB table
        #attributes:  id name content  location time holiday property category salary employee class url
        sql.insert_JOB(str(id_count) , job.name , job.list[1] , category[cate] , job.list[3] , job.list[6] ,\
                        job.list[4], job.list[7] , job.list[2] , location , com.name )

        #Save date into the CORPORATION table
        if sql.getComName(com.name):
            sql.insert_CORPORATION(com.name, com.site, com.address)

        #Id of data +1 
        id_count+=1
    



    #print final result
    print "\n   \n   -- [Finished] --"
    print "   Done ... [" +str(URLnum - urlremove - sql.error )+"/"+str( URLnum ) +"]"
    print "   Webpage not found ... [",urlremove ,'] ' 
    print "   SQL server ERROR ... [",sql.error ,'] \n' 

    #Check log folder, if not exit then create 
    if not os.path.exists('log'): 
         os.makedirs('log')
    

    #Write log and get execution time
    logfile = open('log/log', 'a+')
    logfile.write( str( time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime( time.time() )) )+ \
                           " done-"+str( URLnum - urlremove - sql.error )+"/"+str(URLnum)+\
                           " notfound-"+str(urlremove)+\
                           " serverError-"+str(sql.error)+\
                           " category-"+category[cate]+\
                           "\n"+mainURL+"\n\n" )  


    #Force processing of all buffered & close database server connection
    url_data.close()     
    job.close()  
    logfile.close()
    sql.close_conn()
