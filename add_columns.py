import sqlite3
conn = sqlite3.connect('biat.db')
cur = conn.cursor()
cur.execute("ALTER TABLE requests ADD COLUMN status TEXT;")
cur.execute("ALTER TABLE requests ADD COLUMN responsable_id INTEGER;")
cur.execute("ALTER TABLE requests ADD COLUMN rejection_comment TEXT;")
conn.commit()
conn.close()
print("Columns added successfully.")