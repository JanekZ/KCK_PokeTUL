import unittest
import sqlite3
import os
import tempfile
import shutil

from database.restore import (
    restore_database_from_backup,
    _get_table_columns,
    _get_all_tables,
    restore_all_databases
)

class TestRestore(unittest.TestCase):
    ''' Unit test class for database restoration '''

    def setUp(self) -> None:
        self._temp_dir = tempfile.mkdtemp()
        self._database_dir = os.path.join(self._temp_dir, "database")
        self._data_dir = os.path.join(self._database_dir, "data")
        self._backup_dir = os.path.join(self._database_dir, "backups")

        os.makedirs(self._data_dir)
        os.makedirs(self._backup_dir)

        self._backup_path = os.path.join(self._backup_dir, "test.bak")
        conn = sqlite3.connect(self._backup_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE players (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                level INTEGER DEFAULT 1,
                old_column TEXT
            )
        ''')

        cursor.executemany('''
            INSERT INTO players (id, name, level, old_column)
            VALUES (?, ?, ?, ?)
        ''', [(1, "Alice", 10, "old_data1"), (2, "Bob", 5, "old_data2")])

        conn.commit()
        conn.close()

        self._prod_path = os.path.join(self._data_dir, "test.db")
        conn = sqlite3.connect(self._prod_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE players (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                level INTEGER DEFAULT 1,
                new_column TEXT DEFAULT NULL
            )
        ''')

        conn.commit()
        conn.close()

        self._original_cwd = os.getcwd()
        os.chdir(self._temp_dir)

    def test_get_table_columns(self) -> None:
        conn = sqlite3.connect(self._backup_path)
        cursor = conn.cursor()

        columns = _get_table_columns(cursor, "players")
        self.assertEqual(columns, ["id", "name", "level", "old_column"])

        conn.close()

    def test_get_all_tables(self) -> None:
        conn = sqlite3.connect(self._backup_path)
        cursor = conn.cursor()

        tables = _get_all_tables(cursor)

        self.assertIn("players", tables)
        self.assertEqual(len(tables), 1)

        conn.close()

    def test_restore_basic(self) -> None:
        restore_database_from_backup("test.db")

        conn = sqlite3.connect(self._prod_path)
        cursor = conn.cursor()

        cursor.execute("SELECT id, name, level, new_column FROM players ORDER BY id")
        rows = cursor.fetchall()

        self.assertEqual(rows[0], (1, "Alice", 10, None))
        self.assertEqual(rows[1], (2, "Bob", 5, None))

        conn.close()

    def test_restore_missing_backup(self) -> None:
        os.remove(self._backup_path)

        restore_database_from_backup("test.db")

        conn = sqlite3.connect(self._prod_path)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM players")
        self.assertEqual(cursor.fetchone()[0], 0)

        conn.close()

    def test_restore_missing_production(self) -> None:
        os.remove(self._prod_path)

        restore_database_from_backup("test.db")

        self.assertTrue(os.path.exists(self._backup_path))

    def test_restore_missing_table(self) -> None:
        os.remove(self._prod_path)
        conn = sqlite3.connect(self._prod_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE different_table (
                id INTEGER PRIMARY KEY
            )
        ''')

        conn.commit()
        conn.close()

        restore_database_from_backup("test.db")

        conn = sqlite3.connect(self._prod_path)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM different_table")
        self.assertEqual(cursor.fetchone()[0], 0)

        conn.close()

    def test_restore_no_common_columns(self) -> None:
        os.remove(self._prod_path)
        conn = sqlite3.connect(self._prod_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE players (
                different_id INTEGER PRIMARY KEY,
                different_name TEXT
            )
        ''')

        conn.commit()
        conn.close()

        restore_database_from_backup("test.db")

        conn = sqlite3.connect(self._prod_path)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM players")
        self.assertEqual(cursor.fetchone()[0], 0)

        conn.close()

    def test_restore_empty_backup_table(self) -> None:
        os.remove(self._backup_path)
        conn = sqlite3.connect(self._backup_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE players (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )
        ''')

        conn.commit()
        conn.close()

        restore_database_from_backup("test.db")

        conn = sqlite3.connect(self._prod_path)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM players")
        self.assertEqual(cursor.fetchone()[0], 0)

        conn.close()

    def test_restore_all(self) -> None:
        backup2 = os.path.join(self._backup_dir, "test2.bak")
        conn = sqlite3.connect(backup2)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE items (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )
        ''')

        cursor.executemany('''
            INSERT INTO items (id, name)
            VALUES (?, ?)
        ''', [(1, "sword"), (2, "shield")])

        conn.commit()
        conn.close()

        prod2 = os.path.join(self._data_dir, "test2.db")
        conn = sqlite3.connect(prod2)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE items (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT DEFAULT NULL
            )
        ''')

        conn.commit()
        conn.close()

        restore_all_databases()

        conn = sqlite3.connect(self._prod_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM players")
        count1 = cursor.fetchone()[0]
        conn.close()

        conn = sqlite3.connect(prod2)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM items")
        count2 = cursor.fetchone()[0]
        conn.close()

        self.assertEqual(count1, 2)
        self.assertEqual(count2, 2)

    def test_restore_all_no_backup_dir(self) -> None:
        shutil.rmtree(self._backup_dir)

        restore_all_databases()
        self.assertTrue(True)

    def test_restore_all_empty_backup(self) -> None:
        for f in os.listdir(self._backup_dir):
            os.remove(os.path.join(self._backup_dir, f))

        restore_all_databases()
        self.assertTrue(True)

    def tearDown(self) -> None:
        os.chdir(self._original_cwd)
        shutil.rmtree(self._temp_dir)

if __name__ == "__main__":
    unittest.main()
