# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 10:05:53 2023

@author: tdong
"""

import mysql.connector

cnx = mysql.connector.connect(user='admin',password='ET_5600',host='2600:1700:9120:4a10:ecc4:2935:227f:94f9', database='listflix')
mycursor = cnx.cursor()

"""
Create listflix database
print(cnx)


mycursor.execute("CREATE DATABASE LISTFLIX")

for x in mycursor:
    print(x)
"""
"""
Create users table
mycursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), password VARCHAR(255))")
"""

sql = ("insert into users(username, password) VALUES(%s,%s)")
val = ("User1","Pass1")
mycursor.execute(sql,val)
cnx.commit()

mycursor.execute("select * from users")

for x in mycursor:
    print(x)

cnx.close()