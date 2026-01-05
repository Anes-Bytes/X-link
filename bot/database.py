import sqlite3
import os

class BotDatabase:
    def __init__(self, db_path='bot_data.sqlite3'):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS admins (
                    user_id INTEGER PRIMARY KEY,
                    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS backup_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT
                )
            ''')
            conn.commit()

    def add_admin(self, user_id):
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('INSERT OR IGNORE INTO admins (user_id) VALUES (?)', (user_id,))
                conn.commit()
            return True
        except Exception:
            return False

    def remove_admin(self, user_id):
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('DELETE FROM admins WHERE user_id = ?', (user_id,))
                conn.commit()
            return True
        except Exception:
            return False

    def is_admin(self, user_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('SELECT 1 FROM admins WHERE user_id = ?', (user_id,))
            return cursor.fetchone() is not None

    def get_all_admins(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('SELECT user_id FROM admins')
            return [row[0] for row in cursor.fetchall()]

    def log_backup(self, filename, status):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('INSERT INTO backup_history (filename, status) VALUES (?, ?)', (filename, status))
            conn.commit()
