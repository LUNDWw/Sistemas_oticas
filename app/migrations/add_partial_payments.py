"""
Migration: Add partial_payments table
"""
import sqlite3
from app.config import DB_PATH


def migrate():
    """Create partial_payments table"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create partial_payments table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS partial_payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            payment_date TEXT NOT NULL,
            payment_method TEXT,
            notes TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(order_id) REFERENCES orders(id) ON DELETE CASCADE
        )
    """)
    
    conn.commit()
    conn.close()
    print("Migration completed: partial_payments table created")


if __name__ == '__main__':
    migrate()
