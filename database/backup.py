import os
import shutil

# Create a backup of a specified database
def create_backup(database: str, destination: str) -> None:
    backup = os.path.splitext(os.path.basename(database))[0] + ".bak"
    shutil.copy2(f"database/data/{database}", destination + "/" + backup)

if __name__ == "__main__":
    # Get a list of all available databases
    databases = [database for database in os.listdir("database/data") if os.path.isfile(os.path.join("database/data", database))]

    # Create a 'backup' directory if not exists
    os.makedirs("database/backups", exist_ok=True)

    # Backup all available databases
    for database in databases:
        create_backup(database, "database/backups")
