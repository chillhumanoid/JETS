import mysql.connector

def select(sql):             
    mydb = mysql.connector.connect(
    host="192.168.1.171",
    user="jets-util",
    passwd="utilityaccount",                 #Because this is a utility account that only has permission to run SELECT queries, i dont really care.
    database="jets"
    )
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    mydb.commit()
    return myresult
