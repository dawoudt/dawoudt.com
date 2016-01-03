import mysql.connector


def Connection():
	try:	
		cnx = mysql.connector.connect(user='root', password='root',
	                              host='localhost',
	                              database='Blog')
		cur = cnx.cursor()
		return cur, cnx
	except Exception as e:
		return(str(e))