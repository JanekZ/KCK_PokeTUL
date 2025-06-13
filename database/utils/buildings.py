import sqlite3
import json
from typing import Optional, Any

class Buildings:
    ''' A High Abstraction Layer class for managing buildings data '''

    def __init__(self) -> None:
        self._connection = sqlite3.connect("database/data/constants.db")
        self._connection.row_factory = sqlite3.Row
        self._database = self._connection.cursor()

    def add_building(self, name: str, x: float, y: float, width: float, height: float, color: str = "#FFFFFF") -> bool:
        ''' Inserts a new building into the database '''

        try:
            self._database.execute('''
                INSERT INTO buildings (name, x, y, width, height, color)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, x, y, width, height, color))

            self._connection.commit()

            return True
        except sqlite3.Error:
            return False

    def get_building(self, building_id: int) -> Optional[dict[str, Any]]:
        ''' Retrieves a building by its id '''

        try:
            self._database.execute('''
                SELECT *
                FROM buildings
                WHERE id = ?
            ''', (building_id,))

            building = self._database.fetchone()

            if building is not None:
                return dict(building)

            return None
        except sqlite3.Error:
            return None

    def get_all_buildings(self) -> list[dict[str, Any]]:
        ''' Retrieves all buildings '''

        try:
            self._database.execute('''
                SELECT *
                FROM buildings
            ''')

            return [dict(row) for row in self._database.fetchall()]
        except sqlite3.Error:
            return []

    def update_color(self, building_id: int, color: str) -> bool:
        ''' Updates the color of a building '''

        try:
            self._database.execute('''
                UPDATE buildings
                SET color = ?
                WHERE id = ?
            ''', (color, building_id))

            self._connection.commit()

            return True
        except sqlite3.Error:
            return False

    def delete_building(self, building_id: int) -> bool:
        ''' Deletes a building from the database '''

        try:
            self._database.execute('''
                DELETE FROM buildings
                WHERE id = ?
            ''', (building_id,))

            self._connection.commit()

            return True
        except sqlite3.Error:
            return False

    def __del__(self) -> None:
        self._connection.close()
