import sqlite3

connection = sqlite3.connect("database.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    category TEXT,
    priority TEXT,
    due_date TEXT,
    status TEXT DEFAULT 'Pending',
    user_id INTEGER
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
""")

try:
    cursor.execute("ALTER TABLE users ADD COLUMN otp_code TEXT")
except:
    pass

try:
    cursor.execute("ALTER TABLE users ADD COLUMN otp_expiry TEXT")
except:
    pass

try:
    cursor.execute("""
    ALTER TABLE tasks
    ADD COLUMN reminder_sent INTEGER DEFAULT 0
    """)
except:
    pass

try:
    cursor.execute("""
    ALTER TABLE tasks
    ADD COLUMN user_id INTEGER
    """)
except:
    pass

connection.commit()
connection.close()

#cursor.execute("DROP TABLE IF EXISTS users")

print("Database created successfully!")