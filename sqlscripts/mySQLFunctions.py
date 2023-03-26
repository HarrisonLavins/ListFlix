# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 17:11:27 2023

@author: tdong
"""

import mysql.connector

"""
Insert into listUser table, passing username and password.
example:
    insert_into_listUser('email1@domain.com','user1','pass1')
"""
def insert_into_listUser(email,username,password):
    
    cnx = mysql.connector.connect(user='admin',password='ET_5600',host='localhost', database='LISTFLIX')
    mycursor = cnx.cursor()
    
    # results = []
    # sql = ("SELECT * FROM listUser where email = %s")
    # val = (email)
    # mycursor.execute(sql,val)
    # for x in mycursor:
    #     results.append(x)
        
    # if results.count(x) > 0:
    #     print('that email exists already')
    #     return
    # else:
    sql = ("INSERT INTO listUser(email, username, password) VALUES(%s,%s,%s)")
    val = (email,username,password)
    mycursor.execute(sql,val)
    cnx.commit()

    cnx.close()
    
"""
Insert into listMovie table, passing title
example:
    insert_into_listMovie(['Star Wars'])
"""
def insert_into_listMovie(tmdbid, title, director, releaseDate, posterArt):
    cnx = mysql.connector.connect(user='admin',password='ET_5600',host='localhost', database='LISTFLIX')
    mycursor = cnx.cursor()

    sql = ("INSERT INTO listMovie(tmdbid, title, director, releaseDate, posterArt) VALUES(%s,%s,%s,%s,%s)")
    val = (tmdbid, title, director, releaseDate, posterArt)
    mycursor.execute(sql,val)
    cnx.commit()

    cnx.close()
    
"""
Insert into relUserMovie table, passing userID and movieID
example:
    insert_into_relUserMovie('1','1')
"""
def insert_into_relUserMovie(userID, movieID, ishidden):
    cnx = mysql.connector.connect(user='admin',password='ET_5600',host='localhost', database='LISTFLIX')
    mycursor = cnx.cursor()

    sql = ("INSERT INTO relUserMovie(userID, movieID, ishidden) VALUES(%s,%s,%s)")
    val = (userID, movieID, ishidden)
    mycursor.execute(sql,val)
    cnx.commit()

    cnx.close()
    
"""
Select from users table, passing either id or username, and specifying with the searchtype
#search by id
    select_from_listUser(['3'],'id')
#search by username
    select_from_listUser(['user2'],'user')
#search ALL
    select_from_listUser()
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
        
    cnx.close()
    
    return results
    
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
    elif 'tmdbID' in searchtype:
        sql = sql + "AND tmdbID = %s"
        mycursor.execute(sql,movieparam)
    else:
        sql = sql + "AND movieID = %s"
        mycursor.execute(sql,movieparam)
        
    for x in mycursor:
        results.append(x)
        
    cnx.close()
    
    return results
    
"""
Select from relUserMovie table, passing userID
in the future: specify if searching by ishidden or not
#search by id
    select_from_relUserMovie(['1','0'])
"""

def select_from_relUserMovie(userID,ishidden):
    cnx = mysql.connector.connect(user='admin',password='ET_5600',host='localhost', database='LISTFLIX')
    mycursor = cnx.cursor()
    results = []
    
    sql = ("select lm.tmdbID from listflix.listMovie lm join listflix.relusermovie rum on lm.MovieID = rum.movieID WHERE 1=1 ")
    
    
    sql = sql + "AND userID = %s AND ishidden = %s LIMIT 1000"
    val = (userID, ishidden)
    mycursor.execute(sql,val)
    
    for x in mycursor:
        results.append(x)
        
    cnx.close()
    
    return(results)
    
    
"""
Check if movie exists in listMovie
"""
def check_listMovie(tmdbID):
    cnx = mysql.connector.connect(user='admin',password='ET_5600',host='localhost', database='LISTFLIX')
    mycursor = cnx.cursor()

    rows = select_from_listMovie(tmdbID,'tmdbID')

    if not rows:
        cnx.close()
        return 0
    else:
        cnx.close()
        return 1
    
    

    
    
    
