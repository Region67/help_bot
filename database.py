# database.py
import sqlite3

DB_NAME = 'bot.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            city TEXT,
            is_commercial INTEGER DEFAULT 0,
            joined TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            city TEXT,
            category TEXT,
            description TEXT,
            phone TEXT,
            username TEXT,
            photo_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            active INTEGER DEFAULT 1
        )
    ''')
    conn.commit()
    conn.close()

def get_user(user_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    user = cur.fetchone()
    conn.close()
    return user

def set_user_city(user_id, city):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("INSERT OR REPLACE INTO users (user_id, city) VALUES (?, ?)", (user_id, city))
    conn.commit()
    conn.close()

def create_request(user_id, city, category, description, phone, username, photo_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO requests (user_id, city, category, description, phone, username, photo_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, city, category, description, phone, username, photo_id))
    conn.commit()
    conn.close()

def get_requests_by_city(city, active_only=True):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    if active_only:
        cur.execute("SELECT * FROM requests WHERE city=? AND active=1 AND created_at > datetime('now', '-1 day')", (city,))
    else:
        cur.execute("SELECT * FROM requests WHERE city=?", (city,))
    rows = cur.fetchall()
    conn.close()
    return rows

def get_user_requests(user_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM requests WHERE user_id=?", (user_id,))
    rows = cur.fetchall()
    conn.close()
    return rows

def deactivate_request(request_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("UPDATE requests SET active=0 WHERE id=?", (request_id,))
    conn.commit()
    conn.close()

def count_active_requests(city):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT category, COUNT(*) FROM requests WHERE city=? AND active=1 AND created_at > datetime('now', '-1 day') GROUP BY category", (city,))
    rows = cur.fetchall()
    conn.close()
    return dict(rows)
