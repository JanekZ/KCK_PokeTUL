import sqlite3
import hashlib
import secrets
import time

class Auth:
    ''' A High Abstraction Layer class for handling players authentication '''

    def __init__(self) -> None:
        self._connection = sqlite3.connect("database/data/game.db")
        self._database = self._connection.cursor()

    ''' A method to create a login session '''
    def login(self, player_id: int, password: str) -> tuple[bool, str]:
        try:
            self._database.execute('''
                SELECT id, password, is_banned
                FROM players
                WHERE id = ?
            ''', (player_id,))

            player = self._database.fetchone()

            if player is not None:
                is_banned = player.get("is_banned")

                if is_banned:
                    return False, "Account suspended"

                hashed_password = hashlib.sha256(password.encode()).hexdigest()

                if secrets.compare_digest(hashed_password, player.get("password")):
                    session_id = secrets.token_urlsafe(32)

                    self._database.execute('''
                        INSERT
                        INTO sessions (id, player_id)
                        VALUES (?, ?)
                    ''', (session_id, player_id))

                    self._connection.commit()

                    return True, session_id

            return False, "Invalid credentials"
        except sqlite3.Error as e:
            return False, "Database error"

    ''' A method to create new player '''
    def register(self, index: int, name: str, password: str) -> tuple[bool, str]:
        try:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            self._database.execute('''
                INSERT
                INTO players (id, name, password)
                VALUES (?, ?, ?)
            ''', (index, name, hashed_password))

            self._connection.commit()

            return True, "Registration successful"
        except sqlite3.IntegrityError:
            return False, "Student already exists"
        except sqlite3.Error as e:
            return False, "Database error"

    def __del__(self) -> None:
        self._connection.close()
