import os
from subprocess import call

def get_latest_backup():
    backup_dir = os.path.join(os.getcwd(), "backups")
    if not os.path.exists(backup_dir):
        print("No backups folder found.")
        return None
    
    # Find all SQL files in the backups directory
    backup_files = [f for f in os.listdir(backup_dir) if f.endswith('.sql')]
    if not backup_files:
        print("No backup files found.")
        return None
    
    # Get the latest backup file by timestamp
    latest_backup = max(backup_files, key=lambda x: os.path.getctime(os.path.join(backup_dir, x)))
    return os.path.join(backup_dir, latest_backup)

def restore_db():
    backup_file = get_latest_backup()
    if not backup_file:
        print("No backup file to restore.")
        return

    db_url = os.getenv('DATABASE_URL', 'sqlite:///annotations.db')

    if 'sqlite' in db_url:
        db_path = db_url.split("///")[-1]
        call(["sqlite3", db_path, f".restore {backup_file}"])
    elif 'postgresql' in db_url:
        call(["psql", db_url, "-f", backup_file])

    print(f"Database restored from: {backup_file}")

if __name__ == "__main__":
    restore_db()

# #!/bin/bash
# python backup_db.py  # Create a backup
# # Deploy your application here (e.g., git push or CI/CD commands)
# python restore_db.py  # Restore from backup
