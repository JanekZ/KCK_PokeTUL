from json.decoder import JSONDecodeError, JSONDecoder
import sqlite3
import json

from typing import Optional, Any

class Players:
    ''' A High Abstraction Layer class for managing players interactions '''

    def __init__(self) -> None:
        self._connection = sqlite3.connect("database/data/game.db")
        self._database = self._connection.cursor()

    def get_player(self, player_id: int) -> Optional[dict[str, Any]]:
        ''' Retrieves basic player data '''

        try:
            self._database.execute('''
                SELECT id, name, level, last_x, last_y, unlocked_buildings
                FROM players
                WHERE id = ?
            ''', (player_id,))

            player = self._database.fetchone()

            if player is not None:
                return dict(player)

            return None
        except sqlite3.Error:
            return None

    def update_position(self, player_id: int, x: int, y: int) -> bool:
        ''' Update player's last known position '''

        try:
            self._database.execute('''
                UPDATE players
                SET last_x = ?, last_y = ?
                WHERE id = ?
            ''', (x, y, player_id))

            self._connection.commit()

            return True
        except sqlite3.Error:
            return False

    def level_up(self, player_id: int) -> bool:
        ''' Increase player's level by 1 '''

        try:
            self._database.execute('''
                UPDATE players
                SET level = level + 1
                WHERE id = ?
            ''', (player_id,))

            self._connection.commit()

            return True
        except sqlite3.Error:
            return False

    def ban(self, player_id: int) -> bool:
        ''' Bans the specified player '''

        try:
            self._database.execute('''
                UPDATE players
                SET is_banned = 1
                WHERE id = ?
            ''', (player_id,))

            self._connection.commit()

            return True
        except sqlite3.Error:
            return False

    def discover_building(self, player_id: int, building_id: int) -> bool:
        ''' Marks the specified building as discovered by the player '''

        try:
            self._database.execute('''
                SELECT unlocked_buildings
                FROM players
                WHERE id = ?
            ''', (player_id,))

            unlocked_buildings = self._database.fetchone()

            if unlocked_buildings is not None:
                unlocked_buildings = json.loads(unlocked_buildings.get("unlocked_buildings"))
            else:
                unlocked_buildings = []

            if building_id not in unlocked_buildings:
                unlocked_buildings.append(building_id)

            self._database.execute('''
                UPDATE players
                SET unlocked_buildings = ?
                WHERE id = ?
            ''', (json.dumps(unlocked_buildings), player_id))

            self._connection.commit()

            return True
        except json.JSONDecodeError:
            return False
        except sqlite3.Error:
            return False

    def get_discovered_buildings(self, player_id: int) -> list[int]:
        ''' Returns a list of buildings discovered by the player '''

        try:
            self._database.execute('''
                SELECT unlocked_buildings
                FROM players
                WHERE id = ?
            ''', (player_id,))

            unlocked_buildings = self._database.fetchone()

            if unlocked_buildings is not None:
                return json.loads(unlocked_buildings.get("unlocked_buildings"))

            return []
        except json.JSONDecodeError:
            return []
        except sqlite3.Error:
            return []

    def add_monster(self, player_id: int, monster_type: int, nickname: str = "") -> bool:
        ''' Adds a new monster to the user's collection '''

        try:
            self._database.execute('''
                INSERT
                INTO monsters (player_id, type, nickname, level)
                VALUES (?, ?, ?, 1)
            ''', (player_id, monster_type, nickname))

            self._connection.commit()

            return True
        except sqlite3.Error:
            return False

    def get_monsters(self, player_id: int) -> list[dict[str, Any]]:
        ''' Retrieves a list of all monsters belonging to the player '''

        try:
            self._database.execute('''
                SELECT id, type, nickname, level
                FROM monsters
                WHERE player_id = ?
            ''', (player_id,))

            return [dict(row) for row in self._database.fetchall()]
        except sqlite3.Error:
            return []

    def update_monster(self, monster_id: int, **kwargs) -> bool:
        ''' Updates specified monster attributes '''

        valid_fields = ["nickname", "level"]

        updates = {key: value for key, value in kwargs.items() if key in valid_fields}

        if updates is not None:
            query_keys = ', '.join([f"{key} = ?" for key in updates])

            query_values = list(updates.values())
            query_values.append(monster_id)

            try:
                self._database.execute(f'''
                    UPDATE monsters
                    SET {query_keys}
                    WHERE id = ?
                ''', query_values)

                self._connection.commit()

                return True
            except sqlite3.Error:
                return False

        return False

    def add_item(self, player_id: int, item_id: int, quantity: int = 1) -> bool:
        ''' Adds an item to the player's inventory '''

        try:
            self._database.execute('''
                SELECT quantity
                FROM inventory
                WHERE player_id = ? AND item_id = ?
            ''', (player_id, item_id))

            item = self._database.fetchone()

            if item is not None:
                self._database.execute(f'''
                    UPDATE inventory
                    SET quantity = quantity + {quantity}
                    WHERE player_id = ? AND item_id = ?
                ''', (player_id, item_id))
            else:
                self._database.execute('''
                    INSERT
                    INTO inventory (player_id, item_id, quantity)
                    VALUES (?, ?, ?)
                ''', (player_id, item_id, quantity))

            self._connection.commit()

            return True
        except sqlite3.Error:
            return False

    def remove_item(self, player_id: int, item_id: int, quantity: int = 1) -> bool:
        ''' Removes an item from user's inventory '''

        try:
            self._database.execute('''
                SELECT quantity
                FROM inventory
                WHERE player_id = ? AND item_id = ?
            ''', (player_id, item_id))

            item = self._database.fetchone()

            if item is not None:
                if item.get("quantity") - quantity <= 0:
                    try:
                        self._database.execute('''
                            DELETE
                            FROM inventory
                            WHERE player_id = ? AND item_id = ?
                        ''', (player_id, item_id))
                    except sqlite3.Error:
                        return False
                else:
                    try:
                        self._database.execute(f'''
                            UPDATE inventory
                            SET quantity = quantity - {quantity}
                            WHERE player_id = ? AND item_id = ?
                        ''', (player_id, item_id))
                    except sqlite3.Error:
                        return False

                self._connection.commit()

                return True

            return False
        except sqlite3.Error:
            return False

    def get_inventory(self, player_id: int) -> Optional[dict[int, int]]:
        ''' Retrieves the player's inventory '''

        try:
            self._database.execute('''
                SELECT item_id, quantity
                FROM inventory
                WHERE player_id = ?
            ''', (player_id,))
        except sqlite3.Error:
            return None

        inventory = self._database.fetchall()

        if inventory is not None:
            return {item.get("item_id"): item.get("quantity") for item in inventory}

        return {}

    def player_exists(self, player_id: int) -> bool:
        ''' Checks if player exists '''

        try:
            self._database.execute('''
                SELECT 1
                FROM players
                WHERE id = ?
            ''', (player_id,))

            player = self._database.fetchone()

            if player is not None:
                return True

            return False
        except sqlite3.Error:
            return False

    def is_banned(self, player_id: int) -> bool:
        ''' Checks if player is banned '''

        try:
            self._database.execute('''
                SELECT is_banned
                FROM players
                WHERE id = ?
            ''', (player_id,))

            player = self._database.fetchone()

            if player is not None:
                is_banned = player.get("is_banned")

                return is_banned

            return False
        except sqlite3.Error:
            return False

    def __del__(self) -> None:
        self._connection.close()
