#connect to sqlite database
import sqlite3


# Create a new SQLite database (or connect to an existing one)

conn = sqlite3.connect('survey.db')
cursor = conn.cursor()

# Create a table for the survey results
cursor.execute('''
CREATE TABLE IF NOT EXISTS survey (
    id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER NOT NULL,
    contact_number TEXT NOT NULL,
    favorite_foods TEXT NOT NULL,
    ratings TEXT NOT NULL,
)
''')

conn.commit()
conn.close()

