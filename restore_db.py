import os
import subprocess
import sqlite3

def get_latest_backup():
    backup_dir = os.path.join(os.getcwd(), "backups")
    if not os.path.exists(backup_dir):
        print("No backups folder found.")
        return None
    
    backup_files = [f for f in os.listdir(backup_dir) if f.endswith('.sql')]
    if not backup_files:
        print("No backup files found.")
        return None
    
    latest_backup = max(backup_files, key=lambda x: os.path.getctime(os.path.join(backup_dir, x)))
    return os.path.join(backup_dir, latest_backup)

def clear_existing_tables(db_path):
    """Drop all tables from the SQLite database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("PRAGMA foreign_keys=OFF;")
    cursor.execute("BEGIN TRANSACTION;")
    
    # Fetch all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    # Drop each table
    for table_name in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {table_name[0]}")
    
    conn.commit()
    conn.close()
    print("All existing tables have been cleared.")

def restore_db():
    backup_file = get_latest_backup()
    if not backup_file:
        print("No backup file to restore.")
        return

    db_url = os.getenv('DATABASE_URL', 'sqlite:///annotations.db')

    if 'sqlite' in db_url:
        db_path = db_url.split("///")[-1]
        
        # Clear existing tables in the SQLite database
        clear_existing_tables(db_path)
        
        with open(backup_file, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        # Execute the SQL script to restore the database
        process = subprocess.Popen(['sqlite3', db_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
        stdout, stderr = process.communicate(input=sql_script)
        
        if process.returncode != 0:
            print(f"Error restoring database: {stderr}")
        else:
            print(f"Database restored successfully from: {backup_file}")
    elif 'postgresql' in db_url:
        process = subprocess.Popen(["psql", db_url, "-f", backup_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            print(f"Error restoring database: {stderr.decode()}")
        else:
            print(f"Database restored successfully from: {backup_file}")

if __name__ == "__main__":
    restore_db()




# #!/bin/bash
# python backup_db.py  # Create a backup
# # Deploy your application here (e.g., git push or CI/CD commands)
# python restore_db.py  # Restore from backup
