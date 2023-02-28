# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 10:05:53 2023

@author: tdong
"""

import mysql.connector

cnx = mysql.connector.connect(user='admin',password='ET_5600',host='localhost')
mycursor = cnx.cursor()

mycursor.execute("CREATE DATABASE LISTFLIX")

cnx.commit()

cnx.close()