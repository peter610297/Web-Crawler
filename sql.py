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
     
     #Return the max id of the table
    def getID(self):
         #Check if table already have  data
         if  not self.conn.execute_scalar("SELECT MAX(id) FROM JOB") :
            return 1
         #Return the max number 
         else :     
            return self.conn.execute_scalar("SELECT MAX(id) FROM JOB") + 1

    def getComName(self, name):
         #Check if table already have  data
         if  not self.conn.execute_scalar("SELECT corp_name FROM CORPORATION WHERE corp_name = '"+name+"' ") :
            return 1
         #Return the max number 
         else :     
            return False


   #Close databse connection
    def close_conn(self):
        self.conn.close()

    '''Data Insert Functions of Database Table.
    ''
    ''
    '''

    #Insert data to the table
    def insert_JOB(self, id, name, c, cla, time, sal, h, req, addr, loc, corpName):
        try:
             self.conn.execute_non_query("INSERT INTO JOB VALUES( '"+id+ "','"+name+ "','"+c+"','"+cla+ "','"+time+ "','"+sal+ "','"+h+ "','"+req+ "','"+addr+ "','"+loc+ "','"+corpName+ "')" )
        except _mssql.MssqlDatabaseException,e:
            self.error += 1

    #Insert data to the table
    def insert_CORPORATION(self, corp_name, site, corp_address):
        try:
             self.conn.execute_non_query("INSERT INTO CORPORATION VALUES( '"+corp_name+ "','"+site+ "','"+corp_address+ "')" )
        except _mssql.MssqlDatabaseException,e:
            self.error += 1


