from database import schemas
from database import backup
from database import restore

# Define the specified database schema
def run_migrate(schema) -> None:
    try:
        schema.delete()
    except:
        print(f"Could not delete '{str(schema)}'")
    try:
        schema.define()
    except:
        print(f"Could not define '{str(schema)}'")

# Migrate all available schemas
if __name__ == "__main__":
    print("== Database Migration Process ==")

    # Backup all existing databases
    print("\n\tCreating backups of existing databases...")
    backup.backup_all()
    print("\tBackups created successfully!")

    # Migrate the schemas (delete and recreate)
    print("\n\tMigrating database schemas...")

    print("\tMigrating game schema...")
    run_migrate(schemas.game)

    print("\tMigrating constants schema...")
    run_migrate(schemas.constants)

    print("\tSchema migration completed!")

    # Restore data from backups
    print("\n\tRestoring data from backups...")
    restore.restore_all_databases()

    print("\n== Migration Process Completed Successfully! ==")
