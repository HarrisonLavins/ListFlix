# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 16:47:44 2023

@author: tdong
"""

import mysql.connector
from mySQLFunctions import *

# cnx = mysql.connector.connect(user='admin',password='ET_5600',host='localhost', database='LISTFLIX')
get_connection()
cnx = _connection
mycursor = cnx.cursor()

#Users
mycursor.execute("CREATE TABLE IF NOT EXISTS listUser (userID INT AUTO_INCREMENT PRIMARY KEY, email varchar(255) UNIQUE, username VARCHAR(255), password VARCHAR(255))")

#Movies
mycursor.execute("CREATE TABLE IF NOT EXISTS listMovie (movieID INT AUTO_INCREMENT PRIMARY KEY, tmdbID INT, title VARCHAR(255), director VARCHAR(255), releaseDate DATE, posterArt VARCHAR(255))")

#Genres
mycursor.execute("CREATE TABLE IF NOT EXISTS listGenre (genreID INT AUTO_INCREMENT PRIMARY KEY, genrename VARCHAR(255))")

#relUserMovie
mycursor.execute("CREATE TABLE IF NOT EXISTS relUserMovie (relUserMovieID INT AUTO_INCREMENT PRIMARY KEY, userID INT, movieID INT, isHidden INT)")

#relMovieGenre
mycursor.execute("CREATE TABLE IF NOT EXISTS relMovieGenre (relMovieGenreID INT AUTO_INCREMENT PRIMARY KEY, movieID INT, genreID INT)")



cnx.commit()

# cnx.close()