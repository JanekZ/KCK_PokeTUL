import sqlite3
import hashlib
import secrets
import uuid
from datetime import datetime, timedelta

import engine.constants as c

class Auth:
    ''' A High Abstraction Layer class for handling players authentication '''

    def __init__(self) -> None:
        self._connection = sqlite3.connect("database/data/game.db")
        self._connection.row_factory = sqlite3.Row
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
                is_banned = player["is_banned"]

                if is_banned:
                    return False, "Account suspended"

                hashed_password = hashlib.sha256(password.encode()).hexdigest()

                if secrets.compare_digest(hashed_password, player["password"]):
                    session_id = str(uuid.uuid4())

                    self.store_session(player_id, session_id)

                    return True, session_id

            return False, "Invalid credentials"
        except sqlite3.Error:
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
        except sqlite3.Error:
            return False, "Database error"

    ''' A method to store current user's login session '''
    def store_session(self, player_id: int, session_id: str) -> bool:
        try:
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            self._database.execute('''
                INSERT
                INTO sessions (id, player_id, created)
                VALUES (?, ?, ?)
            ''', (session_id, player_id, date))

            self._connection.commit()

            return True
        except sqlite3.Error as e:
            return False

    ''' A method to validate login session '''
    def validate_session(self, session_id: str) -> bool:
        try:
            self._database.execute('''
                SELECT id, player_id, created
                FROM sessions
                WHERE id = ?
            ''', (session_id,))

            session = self._database.fetchone()

            if session is None:
                return False

            created_time = datetime.strptime(session["created"], "%Y-%m-%d %H:%M:%S")

            if datetime.now() - created_time > timedelta(seconds=c.SESSION_DURATION_SECONDS):
                    self.invalidate_session(session_id)

                    return False

            self._database.execute('''
                SELECT is_banned
                FROM players
                WHERE id = ?
            ''', (session["player_id"],))

            player = self._database.fetchone()

            if player is not None and player["is_banned"] == 0:
                return True

            return False
        except sqlite3.Error:
            return False

    def invalidate_session(self, session_id: str) -> bool:
        try:
            self._database.execute('''
                DELETE
                FROM sessions
                WHERE id = ?
            ''', (session_id,))

            self._connection.commit()

            return True
        except sqlite3.Error:
            return False

    def __del__(self) -> None:
        self._connection.close()
