import os
import sqlite3

from typing import Optional

def _get_table_columns(cursor: sqlite3.Cursor, table_name: str) -> list[str]:
    '''Returns the column names of a given table'''
    try:
        cursor.execute(f'''
            PRAGMA table_info({table_name})
        ''')

        return [column[1] for column in cursor.fetchall()]
    except sqlite3.Error:
        return []


def _get_all_tables(cursor: sqlite3.Cursor) -> list[str]:
    '''Returns all table names in the connected database'''
    try:
        cursor.execute('''
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
        ''')

        return [table[0] for table in cursor.fetchall()]
    except sqlite3.Error:
        return []


def _table_exists(cursor: sqlite3.Cursor, table_name: str) -> bool:
    '''Checks if a table exists in the database'''
    try:
        cursor.execute('''
            SELECT name
            FROM sqlite_master
            WHERE type = 'table' AND name = ?
        ''', (table_name,))

        return cursor.fetchone() is not None
    except sqlite3.Error:
        return False


def restore_database_from_backup(database_name: str) -> None:
    '''Restores a production database using its .bak backup if available'''
    backup_path = f"database/backups/{os.path.splitext(database_name)[0]}.bak"
    production_path = f"database/data/{database_name}"

    if not os.path.exists(backup_path):
        print(f"Backup not found: {backup_path}")
        return

    if not os.path.exists(production_path):
        print(f"Production DB not found: {production_path}")
        return

    print(f"Restoring: {database_name}")

    backup_conn = sqlite3.connect(backup_path)
    prod_conn = sqlite3.connect(production_path)

    backup_conn.row_factory = sqlite3.Row
    prod_conn.row_factory = sqlite3.Row

    backup_cursor = backup_conn.cursor()
    prod_cursor = prod_conn.cursor()

    try:
        tables = _get_all_tables(backup_cursor)

        for table in tables:
            print(f"  Table: {table}")

            if not _table_exists(prod_cursor, table):
                print(f"    Skipped (not found in prod): {table}")
                continue

            backup_columns = _get_table_columns(backup_cursor, table)
            prod_columns = _get_table_columns(prod_cursor, table)

            if not backup_columns:
                print(f"    Skipped (no columns in backup): {table}")
                continue

            common_columns = [col for col in backup_columns if col in prod_columns]

            if not common_columns:
                print(f"    Skipped (no common columns): {table}")
                continue

            try:
                backup_cursor.execute(f'''
                    SELECT {', '.join(backup_columns)}
                    FROM {table}
                ''')

                rows = backup_cursor.fetchall()
            except sqlite3.Error:
                print(f"    Failed to fetch rows from: {table}")
                continue

            if not rows:
                print(f"    No data to restore in: {table}")
                continue

            placeholders = ', '.join(['?' for _ in prod_columns])
            column_list = ', '.join(prod_columns)

            insert_sql = f'''
                INSERT OR IGNORE INTO {table} ({column_list})
                VALUES ({placeholders})
            '''

            transformed = []

            for row in rows:
                transformed_row = []

                for column in prod_columns:
                    value = row[column] if column in row.keys() else None
                    transformed_row.append(value)

                transformed.append(tuple(transformed_row))

            try:
                prod_cursor.executemany(insert_sql, transformed)

                print(f"    Inserted rows: {len(transformed)}")
            except sqlite3.Error as e:
                print(f"    Insert failed for {table}: {e}")
                continue

            missing_in_prod = [col for col in backup_columns if col not in prod_columns]
            new_in_prod = [col for col in prod_columns if col not in backup_columns]

            if missing_in_prod:
                print(f"    Columns missing in prod: {missing_in_prod}")
            if new_in_prod:
                print(f"    New columns in prod (NULL): {new_in_prod}")

        prod_conn.commit()

        print(f"Restoration completed: {database_name}")
    except Exception as e:
        print(f"Error restoring {database_name}: {e}")

        prod_conn.rollback()
    finally:
        backup_conn.close()
        prod_conn.close()


def restore_all_databases() -> None:
    '''Restores all databases from the backups directory'''
    backup_dir = "database/backups"

    if not os.path.exists(backup_dir):
        print("Backup directory missing.")
        return

    backups = [backup for backup in os.listdir(backup_dir) if backup.endswith('.bak')]

    if not backups:
        print("No backup files found.")
        return

    print("Restoring all databases...")

    for backup_file in backups:
        db_name = os.path.splitext(backup_file)[0] + ".db"
        restore_database_from_backup(db_name)

    print("All restorations complete.")

if __name__ == "__main__":
    restore_all_databases()
