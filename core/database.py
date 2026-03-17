import sqlite3
from core.config import Config

def init_db():
    conn = sqlite3.connect(Config.DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trend_name TEXT,
            title TEXT,
            content TEXT,
            image_url TEXT,
            wp_post_id INTEGER,
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trends (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            source TEXT,
            potential_score REAL,
            processed INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_trend(name, source, score):
    conn = sqlite3.connect(Config.DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT OR IGNORE INTO trends (name, source, potential_score) VALUES (?, ?, ?)', (name, source, score))
        conn.commit()
    except Exception as e:
        print(f"Error saving trend: {e}")
    finally:
        conn.close()

def get_unprocessed_trends(limit=5):
    conn = sqlite3.connect(Config.DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT name, source, potential_score FROM trends WHERE processed = 0 ORDER BY potential_score DESC LIMIT ?', (limit,))
    trends = cursor.fetchall()
    conn.close()
    return trends

def mark_trend_processed(name):
    conn = sqlite3.connect(Config.DB_PATH)
    cursor = conn.cursor()
    cursor.execute('UPDATE trends SET processed = 1 WHERE name = ?', (name,))
    conn.commit()
    conn.close()

def save_article(trend_name, title, content, image_url, wp_id):
    conn = sqlite3.connect(Config.DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO articles (trend_name, title, content, image_url, wp_post_id, status) VALUES (?, ?, ?, ?, ?, ?)', 
                   (trend_name, title, content, image_url, wp_id, 'published'))
    conn.commit()
    conn.close()
