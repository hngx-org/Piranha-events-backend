import mysql.connector

cnx = mysql.connector.connect(user='username', password='password',
                              host='ls-748579094099b0766a964caacd8cc4a4b73ec231.czwhjvdkncwk.us-east-2.rds.amazonaws.com',
                              database='database_name')
cursor = cnx.cursor()

query = ("SELECT * FROM table_name")

cursor.execute(query)

for row in cursor:
  print(row)

cursor.close()
cnx.close()
