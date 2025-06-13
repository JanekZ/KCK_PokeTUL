import unittest
import sqlite3
import hashlib
from database.utils.auth import Auth

class TestAuth(unittest.TestCase):
    ''' Unit test class for Auth authentication handler '''

    def setUp(self) -> None:
        self._connection = sqlite3.connect(":memory:")
        self._connection.row_factory = sqlite3.Row
        self._database = self._connection.cursor()

        self._database.execute('''
            CREATE TABLE players (
                id INTEGER PRIMARY KEY NOT NULL UNIQUE,
                name TEXT NOT NULL,
                password TEXT NOT NULL,
                is_banned INTEGER DEFAULT 0
            )
        ''')

        self._database.execute('''
            CREATE TABLE sessions (
                id TEXT PRIMARY KEY UNIQUE,
                player_id INTEGER NOT NULL,
                FOREIGN KEY (player_id) REFERENCES players(id)
            )
        ''')

        self._connection.commit()

        self._auth = Auth()
        self._auth._connection = self._connection
        self._auth._database = self._database

    def test_register_success(self) -> None:
        status, message = self._auth.register(1, "Alice", "securepass")
        self.assertTrue(status)
        self.assertEqual(message, "Registration successful")

    def test_register_duplicate(self) -> None:
        self._auth.register(1, "Alice", "securepass")
        status, message = self._auth.register(1, "Alice", "securepass")
        self.assertFalse(status)
        self.assertEqual(message, "Student already exists")

    def test_login_success(self) -> None:
        hashed = hashlib.sha256("securepass".encode()).hexdigest()
        self._database.execute('''
            INSERT INTO players (id, name, password)
            VALUES (?, ?, ?)
        ''', (1, "Alice", hashed))

        self._connection.commit()

        status, session = self._auth.login(1, "securepass")
        self.assertTrue(status)
        self.assertIsInstance(session, str)

    def test_login_wrong_password(self) -> None:
        hashed = hashlib.sha256("securepass".encode()).hexdigest()
        self._database.execute('''
            INSERT INTO players (id, name, password)
            VALUES (?, ?, ?)
        ''', (1, "Alice", hashed))

        self._connection.commit()

        status, message = self._auth.login(1, "wrongpass")
        self.assertFalse(status)
        self.assertEqual(message, "Invalid credentials")

    def test_login_banned_account(self) -> None:
        hashed = hashlib.sha256("securepass".encode()).hexdigest()
        self._database.execute('''
            INSERT INTO players (id, name, password, is_banned)
            VALUES (?, ?, ?, ?)
        ''', (1, "Alice", hashed, 1))

        self._connection.commit()

        status, message = self._auth.login(1, "securepass")
        self.assertFalse(status)
        self.assertEqual(message, "Account suspended")

    def test_validate_session_valid(self) -> None:
        self._database.execute('''
            INSERT INTO players (id, name, password)
            VALUES (?, ?, ?)
        ''', (1, "Alice", "irrelevant"))

        self._database.execute('''
            INSERT INTO sessions (id, player_id)
            VALUES (?, ?)
        ''', ("abc123", 1))

        self._connection.commit()

        self.assertTrue(self._auth.validate_session("abc123"))

    def test_validate_session_invalid(self) -> None:
        self.assertFalse(self._auth.validate_session("invalid-token"))

    def test_validate_session_banned_player(self) -> None:
        self._database.execute('''
            INSERT INTO players (id, name, password, is_banned)
            VALUES (?, ?, ?, ?)
        ''', (1, "Alice", "irrelevant", 1))

        self._database.execute('''
            INSERT INTO sessions (id, player_id)
            VALUES (?, ?)
        ''', ("abc123", 1))

        self._connection.commit()

        self.assertFalse(self._auth.validate_session("abc123"))

    def tearDown(self) -> None:
        self._connection.close()

if __name__ == "__main__":
    unittest.main()
