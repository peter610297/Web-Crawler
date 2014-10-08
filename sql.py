# -*- coding: UTF-8 -*-

#host: 140.116.86.51
#account : sa
#password : imilab0936200028*

import _mssql
server = "140.116.86.51"
user = "sa"
password = "imilab0936200028*"
db = "IMI_db_project"

conn = None
conn = _mssql.connect(server='140.116.86.51', user='sa', password='imilab0936200028*', database=db)
'''
a ='fuck you all'
insert = "INSERT INTO test VALUES('"+a+ "')"
print insert 
print type(a)
conn.execute_non_query("INSERT INTO test VALUES('"+a+ "')")
'''