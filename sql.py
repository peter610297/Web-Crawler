# -*- coding: UTF-8 -*-

import _mssql

class MS_SQL():
    def __init__(self, h,u,p,d):
        self.host = h         #Host
        self.user = u         #User
        self.db = d            #Database
        self.password = p    #Password
        self.conn = None     #Connection
        self.error = 0

    #Build connection to the database
    def connect(self):
        self.conn = _mssql.connect(server=self.host, user=self.user, password=self.password, database=self.db)
     
    #Insert data to the table
    def insert(self, id, name, c, loc, time, h, p, cate, sal, emp, cla, url):
        try:
             self.conn.execute_non_query("INSERT INTO result VALUES( '"+id+ "','"+name+ "','"+c+ "','"+loc+ "','"+time+ "','"+h+ "',\
        	                                                                                                       '"+p+ "','"+cate+ "','"+sal+ "','"+emp+ "','"+cla+ "','"+url+ "')" )
        except _mssql.MssqlDatabaseException,e:
        	self.error += 1

   #Close databse connection
    def close_conn(self):
        self.conn.close()
