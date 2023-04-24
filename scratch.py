from sqlscripts.mySQLFunctions import *

# cnx = mysql.connector.connect(user='admin',password='ET_5600',host='localhost', database='LISTFLIX')
# cnx = get_connection()
# mycursor = cnx.cursor()

movies = select_from_listMovie([1111], 'tmdbID')
print(movies)