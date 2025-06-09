import unittest
from unittest.mock import patch
from database import migrate

class TestMigration(unittest.TestCase):
    @patch("database.schemas.constants.define")
    @patch("database.schemas.constants.delete")
    def test_run_migrate_constants(self, mock_delete, mock_define):
        migrate.run_migrate(migrate.schemas.constants)
        mock_delete.assert_called_once()
        mock_define.assert_called_once()

    @patch("database.schemas.game.define")
    @patch("database.schemas.game.delete")
    def test_run_migrate_game(self, mock_delete, mock_define):
        migrate.run_migrate(migrate.schemas.game)
        mock_delete.assert_called_once()
        mock_define.assert_called_once()

    @patch("database.schemas.constants.define", side_effect=Exception("Define failed"))
    @patch("database.schemas.constants.delete", side_effect=Exception("Delete failed"))
    def test_run_migrate_handles_exceptions(self, mock_delete, mock_define):
        migrate.run_migrate(migrate.schemas.constants)
        mock_delete.assert_called_once()
        mock_define.assert_called_once()
