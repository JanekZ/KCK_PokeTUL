import sqlite3
from typing import Optional, Any

class Items:
    ''' A High Abstraction Layer class for managing items '''

    def __init__(self) -> None:
        self._connection = sqlite3.connect("database/data/constants.db")
        self._connection.row_factory = sqlite3.Row
        self._database = self._connection.cursor()

    def add_item(self, name: str, effect: str) -> bool:
        ''' Adds a new item '''

        try:
            self._database.execute('''
                INSERT INTO items (name, effect)
                VALUES (?, ?)
            ''', (name, effect))

            self._connection.commit()

            return True
        except sqlite3.Error:
            return False

    def get_item(self, item_id: int) -> Optional[dict[str, Any]]:
        ''' Retrieves an item by id '''

        try:
            self._database.execute('''
                SELECT *
                FROM items
                WHERE id = ?
            ''', (item_id,))

            item = self._database.fetchone()

            if item is not None:
                return dict(item)

            return None
        except sqlite3.Error:
            return None

    def get_all_items(self) -> list[dict[str, Any]]:
        ''' Retrieves all items '''

        try:
            self._database.execute('''
                SELECT *
                FROM items
            ''')

            return [dict(row) for row in self._database.fetchall()]
        except sqlite3.Error:
            return []

    def delete_item(self, item_id: int) -> bool:
        ''' Deletes an item '''

        try:
            self._database.execute('''
                DELETE FROM items
                WHERE id = ?
            ''', (item_id,))

            self._connection.commit()

            return True
        except sqlite3.Error:
            return False

    def __del__(self) -> None:
        self._connection.close()
