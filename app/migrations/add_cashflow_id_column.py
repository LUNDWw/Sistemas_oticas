"""
Migration: Add cash_flow_id to partial_payments table
"""
import sqlite3
from app.config import DB_PATH

def migrate():
    """Add cash_flow_id column to partial_payments table"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Check if column already exists
        cursor.execute("PRAGMA table_info(partial_payments)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if 'cash_flow_id' not in columns:
            print("Adding cash_flow_id column...")
            cursor.execute("ALTER TABLE partial_payments ADD COLUMN cash_flow_id INTEGER")
            print("Column added successfully.")
        else:
            print("Column cash_flow_id already exists.")
            
    except Exception as e:
        print(f"Error during migration: {e}")
        
    conn.commit()
    conn.close()

if __name__ == '__main__':
    migrate()
