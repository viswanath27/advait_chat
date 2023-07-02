import sqlite3

# Database connection
def get_db_connection():
    conn = sqlite3.connect('advait_database.db')
    conn.row_factory = sqlite3.Row
    return conn