import os
import shutil

# Create a backup of a specified database
def backup_single(database: str, destination: str) -> None:
    backup = os.path.splitext(os.path.basename(database))[0] + ".bak"
    shutil.copy2(f"database/data/{database}", destination + "/" + backup)

# Create a backup of all databases available
def backup_all() -> None:
    # Get a list of all available databases
    databases = [database for database in os.listdir("database/data") if os.path.isfile(os.path.join("database/data", database))]

    # Create a 'backup' directory if not exists
    os.makedirs("database/backups", exist_ok=True)

    # Backup all available databases
    for database in databases:
        backup_single(database, "database/backups")

if __name__ == "__main__":
    backup_all()
