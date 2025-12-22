import sqlite3
from datetime import datetime

class EventDB:
    def __init__(self, db_name="events.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.create_table()

    def create_table(self):
        query = """CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    event_type TEXT,
                    value REAL)"""
        self.conn.execute(query)
        self.conn.commit()

    def log_event(self, event_type, value):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.conn.execute("INSERT INTO events (timestamp, event_type, value) VALUES (?, ?, ?)",
                          (timestamp, event_type, value))
        self.conn.commit()
        return {"timestamp": timestamp, "type": event_type, "value": value}