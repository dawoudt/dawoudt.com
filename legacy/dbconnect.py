import MySQLdb

def Connection():
	conn = MySQLdb.connect(host = 'localhost', user = 'root', passwd = 'root', db = 'Blog')
	c = conn.cursor()

	return c, conn