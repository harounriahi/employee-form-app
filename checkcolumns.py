import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(users);")
columns = cursor.fetchall()

print("Columns in users table:")
for col in columns:
    print(col)

conn.close()
