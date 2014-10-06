 # -*- coding: UTF-8 -*-
from __future__ import division
import urllib2
import urllib
from sgmllib import SGMLParser
import sys,time
import  os

class ProgressBar():
    def __init__(self, lenth=100):
        self.pointer = 0
        self.width = 50
        self.range = lenth
        self.count = 0

    def __call__(self):
         # x in percent
         self.pointer = int(self.width*(self.count /self.range))
         #return "|" + "#"*self.pointer + "-"*(self.width-self.pointer)+"| %d /"% int(x)+str(self.range)+"  Done"
         sys.stdout.write("|" + "#"*self.pointer + "-"*(self.width-self.pointer)+"|  "+str(self.count )+'/'+str(self.range)+' ('+str(int((self.count /self.range)*100))+'%) Done'+"\r")
         sys.stdout.flush()
         self.count +=1

if __name__ == '__main__':
    pb = ProgressBar(200)
    for i in range(200):
        #os.system('clear')
        #print pb(i)
        pb()
        time.sleep(0.1)
