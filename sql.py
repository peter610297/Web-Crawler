# -*- coding: UTF-8 -*-

#host: 140.116.86.51
#account : sa
#password : imilab0936200028*

import pymssql

database = pymssql.connect(host='140.116.86.51', user='sa', password='imilab0936200028*', database='IMI_db_project')
dbcur=database.cursor()
dbcur.execute('CREATE TABLE test(id INT)')    