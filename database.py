import sqlite3

def init_db():
    conn = sqlite3.connect('jobs.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            company TEXT,
            link TEXT UNIQUE,
            date_found DATE DEFAULT CURRENT_DATE,
            notified BOOLEAN DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()