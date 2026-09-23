import sqlite3
from typing import List, Dict, Any, Optional

class MemoryStore:
    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self._init_db()

    def _init_db(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS chat_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS facts (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                )
            """)

    def add_chat_message(self, role: str, content: str) -> None:
        with self.conn:
            self.conn.execute("INSERT INTO chat_history (role, content) VALUES (?, ?)", (role, content))

    def add_message(self, role: str, content: str) -> None:
        self.add_chat_message(role, content)

    def get_chat_history(self) -> List[Dict[str, str]]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT role, content FROM chat_history ORDER BY id ASC")
        return [{"role": row[0], "content": row[1]} for row in cursor.fetchall()]

    def get_recent_messages(self, limit: Optional[int] = None) -> List[Dict[str, str]]:
        cursor = self.conn.cursor()
        if limit is not None:
            cursor.execute("SELECT role, content FROM (SELECT id, role, content FROM chat_history ORDER BY id DESC LIMIT ?) ORDER BY id ASC", (limit,))
        else:
            cursor.execute("SELECT role, content FROM chat_history ORDER BY id ASC")
        return [{"role": row[0], "content": row[1]} for row in cursor.fetchall()]

    def clear_chat_history(self) -> None:
        with self.conn:
            self.conn.execute("DELETE FROM chat_history")

    def store_fact(self, key: str, value: str) -> None:
        with self.conn:
            self.conn.execute("INSERT OR REPLACE INTO facts (key, value) VALUES (?, ?)", (key, value))

    def get_fact(self, key: str) -> Optional[str]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT value FROM facts WHERE key = ?", (key,))
        row = cursor.fetchone()
        return row[0] if row else None

    def close(self) -> None:
        if self.conn:
            self.conn.close()

    def __del__(self):
        try:
            self.conn.close()
        except Exception:
            pass
