import sqlite3
from typing import Optional, Any

class SpawnPoints:
    ''' A High Abstraction Layer class for managing spawn points '''

    def __init__(self) -> None:
        self._connection = sqlite3.connect("database/data/constants.db")
        self._connection.row_factory = sqlite3.Row
        self._database = self._connection.cursor()

    def add_spawn_point(self, building_id: int, x: float, y: float, spawn_rate: float) -> bool:
        ''' Adds a new spawn point '''

        try:
            self._database.execute('''
                INSERT
                INTO spawn_points (building_id, x, y, spawn_rate)
                VALUES (?, ?, ?, ?)
            ''', (building_id, x, y, spawn_rate))

            self._connection.commit()

            return True
        except sqlite3.Error:
            return False

    def get_spawn_point(self, spawn_point_id: int) -> Optional[dict[str, Any]]:
        ''' Retrieves a spawn point by id '''

        try:
            self._database.execute('''
                SELECT *
                FROM spawn_points
                WHERE id = ?
            ''', (spawn_point_id,))

            spawn_point = self._database.fetchone()

            if spawn_point is not None:
                return dict(spawn_point)

            return None
        except sqlite3.Error:
            return None

    def get_spawn_points_for_building(self, building_id: int) -> list[dict[str, Any]]:
        ''' Retrieves all spawn points for a specific building '''

        try:
            self._database.execute('''
                SELECT *
                FROM spawn_points
                WHERE building_id = ?
            ''', (building_id,))

            return [dict(row) for row in self._database.fetchall()]
        except sqlite3.Error:
            return []

    def get_all_spawn_points(self) -> list:
        ''' Retrieves all spawn points '''

        self._database.execute('''
            SELECT *
            FROM spawn_points
        ''')

        return self._database.fetchall()

    def delete_spawn_point(self, spawn_point_id: int) -> bool:
        ''' Deletes a spawn point '''

        try:
            self._database.execute('''
                DELETE FROM spawn_points
                WHERE id = ?
            ''', (spawn_point_id,))

            self._connection.commit()

            return True
        except sqlite3.Error:
            return False

    def __del__(self) -> None:
        self._connection.close()
