# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 17:11:27 2023

@author: tdong
"""

import mysql.connector

"""
Insert into listUser table, passing username and password.
example:
    insert_into_listUser('user1','pass1')
"""
def insert_into_listUser(username,password):
    
    cnx = mysql.connector.connect(user='admin',password='ET_5600',host='localhost', database='LISTFLIX')
    mycursor = cnx.cursor()

    sql = ("INSERT INTO listUser(username, password) VALUES(%s,%s)")
    val = (username,password)
    mycursor.execute(sql,val)
    cnx.commit()

    cnx.commit()

    cnx.close()
    
"""
Insert into listMovie table, passing title
example:
    insert_into_listMovie(['Star Wars'])
"""
def insert_into_listMovie(title):
    cnx = mysql.connector.connect(user='admin',password='ET_5600',host='localhost', database='LISTFLIX')
    mycursor = cnx.cursor()

    sql = ("INSERT INTO listMovie(title) VALUES(%s)")
    val = (title)
    mycursor.execute(sql,val)
    cnx.commit()

    cnx.commit()

    cnx.close()
    
"""
Insert into relUserMovie table, passing userID and movieID
example:
    insert_into_relUserMovie('1','1')
"""
def insert_into_relUserMovie(userID, movieID):
    cnx = mysql.connector.connect(user='admin',password='ET_5600',host='localhost', database='LISTFLIX')
    mycursor = cnx.cursor()

    sql = ("INSERT INTO listMovie(userID, movieID) VALUES(%s,%s)")
    val = (userID, movieID)
    mycursor.execute(sql,val)
    cnx.commit()

    cnx.commit()

    cnx.close()
    
"""
Select from users table, passing either id or username, and specifying with the searchtype
#search by id
    select_from_users(['3'],'id')
#search by username
    select_from_users(['user2'],'user')
#search ALL
    select_from_users()
"""

def select_from_listUser(userparam: str = None,searchtype: str = 'user'):
    cnx = mysql.connector.connect(user='admin',password='ET_5600',host='localhost', database='LISTFLIX')
    mycursor = cnx.cursor()
    results = []
    
    sql = ("SELECT * FROM listUser WHERE 1=1 ")
    
    if not userparam:
        sql = sql + "LIMIT 1000"
        mycursor.execute(sql)
    elif 'user' in searchtype:
        sql = sql + "AND username = %s LIMIT 1000"
        mycursor.execute(sql,userparam)
    else:
        sql = sql + "AND userID = %s"
        mycursor.execute(sql,userparam)
        
    for x in mycursor:
        results.append(x)
    
    print(results)
    
"""
Select from listMovie table, passing either id or title, and specifying with the searchtype
#search by id
    select_from_listMovie(['1'],'id')
#search by username
    select_from_listMovie(['Star Wars'],'title')
#search ALL
    select_from_listMovie()
"""

def select_from_listMovie(movieparam: str = None,searchtype: str = 'title'):
    cnx = mysql.connector.connect(user='admin',password='ET_5600',host='localhost', database='LISTFLIX')
    mycursor = cnx.cursor()
    results = []
    
    sql = ("SELECT * FROM listMovie WHERE 1=1 ")
    
    if not movieparam:
        sql = sql + "LIMIT 1000"
        mycursor.execute(sql)
    elif 'title' in searchtype:
        sql = sql + "AND title = %s LIMIT 1000"
        mycursor.execute(sql,movieparam)
    else:
        sql = sql + "AND movieID = %s"
        mycursor.execute(sql,movieparam)
        
    for x in mycursor:
        results.append(x)
    
    print(results)
    
select_from_listMovie()
