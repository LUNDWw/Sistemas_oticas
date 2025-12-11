import sqlite3
import os

databases = ['data.db', 'dist/data.db']

for db_path in databases:
    if os.path.exists(db_path):
        print(f"Migrating {db_path}...")
        try:
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            # Check if column exists
            c.execute("PRAGMA table_info(graus)")
            columns = [info[1] for info in c.fetchall()]
            if 'adicao' not in columns:
                print(f"Adding 'adicao' column to {db_path}")
                c.execute("ALTER TABLE graus ADD COLUMN adicao TEXT")
                conn.commit()
            else:
                print(f"'adicao' column already exists in {db_path}")
            conn.close()
        except Exception as e:
            print(f"Error migrating {db_path}: {e}")
    else:
        print(f"{db_path} not found.")
