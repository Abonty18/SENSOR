import os
from datetime import datetime
from subprocess import call

def backup_db():
    # Ensure the backup directory exists
    backup_dir = os.path.join(os.getcwd(), "backups")
    os.makedirs(backup_dir, exist_ok=True)

    # Define backup file name with timestamp
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    backup_file = os.path.join(backup_dir, f"backup_{timestamp}.sql")
    
    # Command to backup SQLite or PostgreSQL (adjust accordingly)
    db_url = os.getenv('DATABASE_URL', 'sqlite:///annotations.db')  # Default to SQLite for local dev
    
    if 'sqlite' in db_url:
        db_path = db_url.split("///")[-1]
        call(["sqlite3", db_path, f".backup {backup_file}"])
    elif 'postgresql' in db_url:
        call(["pg_dump", db_url, "-f", backup_file])

    print(f"Database backup created: {backup_file}")

if __name__ == "__main__":
    backup_db()
