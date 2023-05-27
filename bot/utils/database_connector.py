from mysql.connector import connection

connection_database = connection.MySQLConnection(user='root', password='', host='localhost', database='flask_database')
cursor = connection_database.cursor()
