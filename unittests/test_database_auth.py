import unittest
import sqlite3
import hashlib
from database.utils.auth import Auth

class TestAuth(unittest.TestCase):
    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

        self.cursor.execute('''
            CREATE TABLE players (
                id INTEGER PRIMARY KEY NOT NULL UNIQUE,
                name TEXT NOT NULL,
                password TEXT NOT NULL,
                is_banned INTEGER DEFAULT 0
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE sessions (
                id TEXT PRIMARY KEY UNIQUE,
                player_id INTEGER NOT NULL,
                FOREIGN KEY (player_id) REFERENCES players(id)
            )
        ''')

        self.connection.commit()

        self.auth = Auth()
        self.auth._connection = self.connection
        self.auth._database = self.cursor

    def test_register_status(self):
        status, message = self.auth.register(1, "Alice", "password123")
        self.assertTrue(status)
        self.assertEqual(message, "Registration successful")

    def test_register_duplicate(self):
        self.auth.register(1, "Alice", "password123")
        status, message = self.auth.register(1, "Alice", "password123")
        self.assertFalse(status)
        self.assertEqual(message, "Student already exists")

    def test_login_status(self):
        hashed_pw = hashlib.sha256("password123".encode()).hexdigest()
        self.cursor.execute('''
            INSERT INTO players (id, name, password) VALUES (?, ?, ?)
        ''', (1, "Alice", hashed_pw))
        self.connection.commit()

        status, message = self.auth.login(1, "password123")
        self.assertTrue(status)
        self.assertIsInstance(message, str)
        self.assertGreater(len(message), 0)

    def test_login_invalid_credentials(self):
        hashed_pw = hashlib.sha256("password123".encode()).hexdigest()
        self.cursor.execute('''
            INSERT INTO players (id, name, password) VALUES (?, ?, ?)
        ''', (1, "Alice", hashed_pw))
        self.connection.commit()

        status, message = self.auth.login(1, "wrongpass")
        self.assertFalse(status)
        self.assertEqual(message, "Invalid credentials")

    def test_login_banned_user(self):
        hashed_pw = hashlib.sha256("password123".encode()).hexdigest()
        self.cursor.execute('''
            INSERT INTO players (id, name, password, is_banned)
            VALUES (?, ?, ?, ?)
        ''', (1, "Alice", hashed_pw, 1))
        self.connection.commit()

        status, message = self.auth.login(1, "password123")
        self.assertFalse(status)
        self.assertEqual(message, "Account suspended")

    def test_validate_session_valid(self):
        # Setup valid player and session
        self.cursor.execute('''
            INSERT INTO players (id, name, password) VALUES (?, ?, ?)
        ''', (1, "Alice", "irrelevant"))
        self.cursor.execute('''
            INSERT INTO sessions (id, player_id) VALUES (?, ?)
        ''', ("session-token-xyz", 1))
        self.connection.commit()

        self.assertTrue(self.auth.validate_session("session-token-xyz"))

    def test_validate_session_invalid(self):
        self.assertFalse(self.auth.validate_session("nonexistent-session"))

    def test_validate_session_banned_player(self):
        self.cursor.execute('''
            INSERT INTO players (id, name, password, is_banned) VALUES (?, ?, ?, ?)
        ''', (1, "Alice", "irrelevant", 1))
        self.cursor.execute('''
            INSERT INTO sessions (id, player_id) VALUES (?, ?)
        ''', ("session-token-xyz", 1))
        self.connection.commit()

        self.assertFalse(self.auth.validate_session("session-token-xyz"))

    def tearDown(self):
        self.connection.close()

if __name__ == "__main__":
    unittest.main()
