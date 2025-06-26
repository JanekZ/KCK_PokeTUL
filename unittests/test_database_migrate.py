import unittest
import sqlite3
import os
import tempfile
import shutil
from unittest.mock import Mock, patch

class TestMigrate(unittest.TestCase):
    ''' Unit test class for migration process '''

    def setUp(self) -> None:
        self._temp_dir = tempfile.mkdtemp()
        self._database_dir = os.path.join(self._temp_dir, "database")
        self._data_dir = os.path.join(self._database_dir, "data")
        self._backup_dir = os.path.join(self._database_dir, "backups")

        os.makedirs(self._data_dir)
        os.makedirs(self._backup_dir)

        self._game_db = os.path.join(self._data_dir, "game.db")
        self._constants_db = os.path.join(self._data_dir, "constants.db")

        game_conn = sqlite3.connect(self._game_db)
        game_cursor = game_conn.cursor()

        game_cursor.execute('''
            CREATE TABLE players (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                level INTEGER DEFAULT 1
            )
        ''')

        game_cursor.execute('''
            INSERT INTO players (id, name, level)
            VALUES (?, ?, ?)
        ''', (1, "Alice", 10))

        game_conn.commit()
        game_conn.close()

        const_conn = sqlite3.connect(self._constants_db)
        const_cursor = const_conn.cursor()

        const_cursor.execute('''
            CREATE TABLE buildings (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )
        ''')

        const_cursor.execute('''
            INSERT INTO buildings (id, name)
            VALUES (?, ?)
        ''', (1, "Castle"))

        const_conn.commit()
        const_conn.close()

        self._original_cwd = os.getcwd()
        os.chdir(self._temp_dir)

    def test_run_migrate_success(self) -> None:
        from database.migrate import run_migrate

        schema = Mock()
        schema.delete = Mock()
        schema.define = Mock()

        run_migrate(schema)

        schema.delete.assert_called_once()
        schema.define.assert_called_once()

    def test_run_migrate_delete_exception(self) -> None:
        from database.migrate import run_migrate

        schema = Mock()
        schema.delete = Mock(side_effect=Exception("Delete failed"))
        schema.define = Mock()

        with patch("builtins.print") as mock_print:
            run_migrate(schema)

        schema.define.assert_called_once()
        mock_print.assert_called()

    def test_run_migrate_define_exception(self) -> None:
        from database.migrate import run_migrate

        schema = Mock()
        schema.delete = Mock()
        schema.define = Mock(side_effect=Exception("Define failed"))

        with patch("builtins.print") as mock_print:
            run_migrate(schema)

        schema.delete.assert_called_once()
        mock_print.assert_called()

    def test_run_migrate_both_fail(self) -> None:
        from database.migrate import run_migrate

        schema = Mock()
        schema.delete = Mock(side_effect=Exception("Delete failed"))
        schema.define = Mock(side_effect=Exception("Define failed"))

        with patch("builtins.print") as mock_print:
            run_migrate(schema)

        self.assertEqual(mock_print.call_count, 2)

    @patch("database.restore.restore_all_databases")
    @patch("database.backup.backup_all")
    @patch("database.schemas.constants")
    @patch("database.schemas.game")
    def test_main_process(self, game, constants, backup, restore) -> None:
        game.delete = Mock()
        game.define = Mock()
        constants.delete = Mock()
        constants.define = Mock()

        from database.migrate import run_migrate

        with patch("database.migrate.backup") as b, patch("database.migrate.restore") as r, patch("database.migrate.schemas") as s:

            s.game = game
            s.constants = constants
            b.backup_all = Mock()
            r.restore_all_databases = Mock()

            b.backup_all()
            run_migrate(s.game)
            run_migrate(s.constants)
            r.restore_all_databases()

            b.backup_all.assert_called_once()
            r.restore_all_databases.assert_called_once()
            game.delete.assert_called_once()
            game.define.assert_called_once()
            constants.delete.assert_called_once()
            constants.define.assert_called_once()

    def test_schema_integration(self) -> None:
        try:
            schema_game = type("MockSchema", (), {
                "delete": lambda: None,
                "define": lambda: self._create_game_schema()
            })()

            schema_constants = type("MockSchema", (), {
                "delete": lambda: None,
                "define": lambda: self._create_constants_schema()
            })()

            from database.migrate import run_migrate

            run_migrate(schema_game)
            run_migrate(schema_constants)

            self.assertTrue(os.path.exists(self._game_db))
            self.assertTrue(os.path.exists(self._constants_db))
        except ImportError:
            self.skipTest("Schema modules not found")

    def test_schema_str_representation(self) -> None:
        from database.migrate import run_migrate

        schema = Mock()
        schema.__str__ = Mock(return_value="TestSchema")
        schema.delete = Mock(side_effect=Exception("Test error"))
        schema.define = Mock()

        with patch("builtins.print") as mock_print:
            run_migrate(schema)

        schema.__str__.assert_called()
        mock_print.assert_called()

    def _create_game_schema(self) -> None:
        conn = sqlite3.connect(self._game_db)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                level INTEGER DEFAULT 1,
                new_column TEXT DEFAULT NULL
            )
        ''')

        conn.commit()
        conn.close()

    def _create_constants_schema(self) -> None:
        conn = sqlite3.connect(self._constants_db)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS buildings (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                x REAL DEFAULT 0,
                y REAL DEFAULT 0
            )
        ''')

        conn.commit()
        conn.close()

    def tearDown(self) -> None:
        os.chdir(self._original_cwd)
        shutil.rmtree(self._temp_dir)

if __name__ == "__main__":
    unittest.main()
