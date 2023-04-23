# -*- coding: utf-8 -*-
# """
# Created on Mon Feb 27 17:11:27 2023

# @author: tdong
# """

import mysql.connector

_connection = None

def get_connection():
    global _connection
    if not _connection:
        _connection = mysql.connector.connect(user='admin',password='ET_5600',host='localhost', database='LISTFLIX')
    return _connection


def insert_into_listAccount(email,password):
    cnx = get_connection()
    mycursor = cnx.cursor()
    sql = ("INSERT INTO listAccount(email, password) VALUES(%s,%s)")
    val = (email,password)
    mycursor.execute(sql,val)
    cnx.commit()

def insert_into_listUser(username,profilepic,account):
    cnx = get_connection()
    mycursor = cnx.cursor()
    sql = ("INSERT INTO listUser(username, profilepic, accountID) VALUES(%s,%s,%s)")
    val = (username,profilepic,account)
    mycursor.execute(sql,val)
    cnx.commit()

def insert_into_listMovie(tmdbid, title, director, releaseDate, posterArt):
    get_connection()
    cnx = _connection
    mycursor = cnx.cursor()

    sql = ("INSERT INTO listMovie(tmdbid, title, director, releaseDate, posterArt) VALUES(%s,%s,%s,%s,%s)")
    val = (tmdbid, title, director, releaseDate, posterArt)
    mycursor.execute(sql,val)
    cnx.commit()

def insert_into_relUserMovie(userID, movieID, ishidden):
    get_connection()
    cnx = _connection
    mycursor = cnx.cursor()

    sql = ("INSERT INTO relUserMovie(userID, movieID, ishidden) VALUES(%s,%s,%s)")
    val = (userID, movieID, ishidden)
    mycursor.execute(sql,val)
    cnx.commit()

    
def select_from_listAccount(email):
    cnx =  get_connection()
    mycursor = cnx.cursor()
    sql = ("SELECT AccountID, password FROM listAccount WHERE email = %s")
    mycursor.execute(sql,email)
    result = mycursor.fetchone()
    return result
    
def select_from_listUser(userparam: str = None,searchtype: str = 'account'):
    cnx =  get_connection()
    mycursor = cnx.cursor()
    results = []
    sql = ("SELECT * FROM listUser WHERE 1=1 ")
    if not userparam:
        sql = sql + "LIMIT 1000"
        mycursor.execute(sql)
    elif 'account' in searchtype:
        sql = sql + "AND accountID = %s LIMIT 1000"
        mycursor.execute(sql,userparam)
    else:
        sql = sql + "AND userID = %s"
        mycursor.execute(sql,userparam)
    for x in mycursor:
        results.append(x)
    return results
    
def select_from_listMovie(movieparam: str = None,searchtype: str = 'title'):
    get_connection()
    cnx = _connection
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
    
    return results
    

def select_from_relUserMovie(userID,ishidden):
    get_connection()
    cnx = _connection
    mycursor = cnx.cursor()
    results = []
    
    sql = ("select lm.tmdbID from listflix.listMovie lm join listflix.relusermovie rum on lm.MovieID = rum.movieID WHERE 1=1 ")
    
    
    sql = sql + "AND userID = %s AND ishidden = %s LIMIT 1000"
    val = (userID, ishidden)
    mycursor.execute(sql,val)
    
    for x in mycursor:
        results.append(x)
        
    return(results)
    
    
def check_listMovie(tmdbID):

    rows = select_from_listMovie(tmdbID,'tmdbID')

    if not rows:
        return 0
    else:
        return 1
    
    

    
    
    
