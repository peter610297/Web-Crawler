# -*- coding: UTF-8 -*-

import _mssql

class MS_SQL():
    def __init__(self, h,u,p,d):
        self.host = h         #Host
        self.user = u         #User
        self.db = d            #Database
        self.password = p    #Password
        self.conn = None     #Connection

    #Build connection to the database
    def connect(self):
        self.conn = _mssql.connect(server=self.host, user=self.user, password=self.password, database=self.db)
     
    #Insert data to the table
    def insert(self, id, name, c, loc, time, h, p, cate, sal, emp, cla, url):
        self.conn.execute_non_query("INSERT INTO result VALUES( '"+id+ "','"+name+ "','"+c+ "','"+loc+ "','"+time+ "','"+h+ "',\
        	                                                                                               '"+p+ "','"+cate+ "','"+sal+ "','"+emp+ "','"+cla+ "','"+url+ "')" )
