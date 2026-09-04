import sqlite3

connection = sqlite3.connect("network.db")
cursor = connection.cursor()

cursor.execute("SELECT * FROM devices")
devices = cursor.fetchall()

for device in devices:
    print(device)

connection.close()