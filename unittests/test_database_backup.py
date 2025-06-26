import unittest
import sqlite3
import os
import tempfile
import shutil

from database.backup import backup_single, backup_all

class TestBackup(unittest.TestCase):
    ''' Unit test class for backup operations '''

    def setUp(self) -> None:
        self._temp_dir = tempfile.mkdtemp()
        self._database_dir = os.path.join(self._temp_dir, "database")
        self._data_dir = os.path.join(self._database_dir, "data")
        self._backup_dir = os.path.join(self._database_dir, "backups")

        os.makedirs(self._data_dir)
        os.makedirs(self._backup_dir)

        self._db_path = os.path.join(self._data_dir, "test.db")

        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE players (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                level INTEGER DEFAULT 1
            )
        ''')

        cursor.executemany('''
            INSERT INTO players (id, name, level)
            VALUES (?, ?, ?)
        ''', [(1, "Alice", 10), (2, "Bob", 5)])

        conn.commit()
        conn.close()

        self._original_cwd = os.getcwd()

        os.chdir(self._temp_dir)

    def test_backup_single_success(self) -> None:
        backup_single("test.db", self._backup_dir)

        backup_path = os.path.join(self._backup_dir, "test.bak")
        self.assertTrue(os.path.exists(backup_path))

        conn = sqlite3.connect(backup_path)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM players")
        count = cursor.fetchone()[0]

        self.assertEqual(count, 2)
        conn.close()

    def test_backup_single_file_not_found(self) -> None:
        with self.assertRaises(FileNotFoundError):
            backup_single("invalid.db", self._backup_dir)

    def test_backup_single_destination_missing(self) -> None:
        target_dir = os.path.join(self._temp_dir, "not_exist")

        with self.assertRaises(FileNotFoundError):
            backup_single("test.db", target_dir)

    def test_backup_all_success(self) -> None:
        second_db = os.path.join(self._data_dir, "test2.db")
        conn = sqlite3.connect(second_db)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE items (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )
        ''')

        cursor.execute('''
            INSERT INTO items (id, name)
            VALUES (?, ?)
        ''', (1, "sword"))

        conn.commit()
        conn.close()

        backup_all()

        path1 = os.path.join(self._backup_dir, "test.bak")
        path2 = os.path.join(self._backup_dir, "test2.bak")

        self.assertTrue(os.path.exists(path1))
        self.assertTrue(os.path.exists(path2))

    def test_backup_all_no_data_directory(self) -> None:
        shutil.rmtree(self._data_dir)

        with self.assertRaises(FileNotFoundError):
            backup_all()

    def test_backup_all_empty_directory(self) -> None:
        for file in os.listdir(self._data_dir):
            os.remove(os.path.join(self._data_dir, file))

        backup_all()
        self.assertEqual(len(os.listdir(self._backup_dir)), 0)

    def test_backup_all_creates_backup_directory(self) -> None:
        shutil.rmtree(self._backup_dir)

        backup_all()
        self.assertTrue(os.path.exists(self._backup_dir))

    def test_backup_preserves_metadata(self) -> None:
        stat_original = os.stat(self._db_path)

        backup_single("test.db", self._backup_dir)

        backup_path = os.path.join(self._backup_dir, "test.bak")
        stat_backup = os.stat(backup_path)

        self.assertEqual(stat_original.st_mtime, stat_backup.st_mtime)

    def test_backup_overwrites_existing(self) -> None:
        backup_single("test.db", self._backup_dir)

        path = os.path.join(self._backup_dir, "test.bak")
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO players (id, name, level)
            VALUES (?, ?, ?)
        ''', (3, "Charlie", 7))

        conn.commit()
        conn.close()

        backup_single("test.db", self._backup_dir)

        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM players")
        count = cursor.fetchone()[0]
        conn.close()

        self.assertEqual(count, 3)

    def tearDown(self) -> None:
        os.chdir(self._original_cwd)
        shutil.rmtree(self._temp_dir)

if __name__ == "__main__":
    unittest.main()
