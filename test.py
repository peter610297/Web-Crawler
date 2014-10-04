 # -*- coding: UTF-8 -*-
import urllib2
import urllib
from sgmllib import SGMLParser

b='http://www.1111.com.tw/%E6%97%A9%E9%A4%90%E5%BA%97%E5%84%B2%E5%82%99%E5%BA%97%E9%95%B7%09-%E6%96%B0%E5%8C%97%E5%B8%82-%E6%B1%90%E6%AD%A2%E5%8D%80-%E6%89%BE%E5%B7%A5%E4%BD%9C-77015381.htm'
a=b.replace('%09','%20') 
print a