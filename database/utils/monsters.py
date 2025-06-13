import sqlite3
from typing import Optional, Any

class Monsters:
    ''' A High Abstraction Layer class for managing monsters '''

    def __init__(self) -> None:
        self._connection = sqlite3.connect("database/data/constants.db")
        self._connection.row_factory = sqlite3.Row
        self._database = self._connection.cursor()

    def add_monster_type(self, name: str, base_health: int, base_attack: int, base_defense: int) -> bool:
        ''' Adds a new monster type '''

        try:
            self._database.execute('''
                INSERT INTO monster_types (name, base_health, base_attack, base_defense)
                VALUES (?, ?, ?, ?)
            ''', (name, base_health, base_attack, base_defense))

            self._connection.commit()

            return True
        except sqlite3.Error:
            return False

    def get_monster_type(self, monster_type_id: int) -> Optional[dict[str, Any]]:
        ''' Retrieves monster type by id '''

        try:
            self._database.execute('''
                SELECT *
                FROM monster_types
                WHERE id = ?
            ''', (monster_type_id,))

            monster_type = self._database.fetchone()

            if monster_type is not None:
                return dict(monster_type)

            return None
        except sqlite3.Error:
            return None

    def get_all_monster_types(self) -> list[dict[str, Any]]:
        ''' Retrieves all monster types '''

        try:
            self._database.execute('''
                SELECT *
                FROM monster_types
            ''')

            return [dict(row) for row in self._database.fetchall()]
        except sqlite3.Error:
            return []

    def delete_monster_type(self, monster_type_id: int) -> bool:
        ''' Deletes a monster type '''

        try:
            self._database.execute('''
                DELETE FROM monster_types
                WHERE id = ?
            ''', (monster_type_id,))

            self._connection.commit()

            return True
        except sqlite3.Error:
            return False

    def __del__(self) -> None:
        self._connection.close()
