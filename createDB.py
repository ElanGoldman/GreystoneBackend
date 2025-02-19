import sqlite3

# Connect to (or create) a database
conn = sqlite3.connect("users.db")

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create a table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
    )
""")

# Commit and close connection
conn.commit()
conn.close()
