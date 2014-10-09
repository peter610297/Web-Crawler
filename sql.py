# -*- coding: UTF-8 -*-

#host: 140.116.86.51
#account : sa
#password : imilab0936200028*

import _mssql

class MS_SQL():
    def __init__(self, h,u,p,d):
        self.host = h
        self.user = u
        self.password = p
        self.db = d
        self.conn = None

    def connect(self):
        self.conn = _mssql.connect(server=self.host, user=self.user, password=self.password, database=self.db)

#    def insert(self, n):
 #      self.conn.execute_non_query("INSERT INTO test VALUES('"+n+ "')")


    def insert(self, id, name, c, loc, time, h, p, cate, sal, emp, cla, url):
        self.conn.execute_non_query("INSERT INTO result VALUES( '"+id+ "','"+name+ "','"+c+ "','"+loc+ "','"+time+ "','"+h+ "',\
        	                                                                                               '"+p+ "','"+cate+ "','"+sal+ "','"+emp+ "','"+cla+ "','"+url+ "')" )
