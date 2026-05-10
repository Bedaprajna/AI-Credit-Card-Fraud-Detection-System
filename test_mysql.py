import mysql.connector

print("Trying Connection...")

try:

    db = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Mysql@2005",
        database="fraud_detection",
        connection_timeout=5
    )

    print("CONNECTED SUCCESSFULLY")

except Exception as e:

    print("ERROR:")
    print(e)