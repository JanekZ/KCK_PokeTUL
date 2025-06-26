import unittest
import sqlite3
from database.utils.buildings import Buildings
from database.utils.monsters import Monsters
from database.utils.items import Items
from database.utils.spawn_points import SpawnPoints

class TestConstantsUtils(unittest.TestCase):
    ''' Unit test class for constants.db utility handlers '''

    def setUp(self) -> None:
        self._connection = sqlite3.connect(":memory:")
        self._connection.row_factory = sqlite3.Row
        self._database = self._connection.cursor()

        self._database.executescript('''
            CREATE TABLE buildings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                x REAL NOT NULL,
                y REAL NOT NULL,
                width REAL NOT NULL,
                height REAL NOT NULL,
                color TEXT NOT NULL DEFAULT '#FFFFFF'
            );

            CREATE TABLE monster_types (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                base_health INTEGER NOT NULL,
                base_attack INTEGER NOT NULL,
                base_defense INTEGER NOT NULL
            );

            CREATE TABLE items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                effect TEXT NOT NULL
            );

            CREATE TABLE spawn_points (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                building_id INTEGER NOT NULL,
                x REAL NOT NULL,
                y REAL NOT NULL,
                spawn_rate REAL NOT NULL,
                FOREIGN KEY (building_id) REFERENCES buildings(id)
            );
        ''')

        self._connection.commit()

        self._buildings = Buildings()
        self._buildings._connection = self._connection
        self._buildings._database = self._database

        self._monster_types = Monsters()
        self._monster_types._connection = self._connection
        self._monster_types._database = self._database

        self._items = Items()
        self._items._connection = self._connection
        self._items._database = self._database

        self._spawn_points = SpawnPoints()
        self._spawn_points._connection = self._connection
        self._spawn_points._database = self._database

    def test_add_and_get_building(self) -> None:
        self.assertTrue(self._buildings.add_building("Tower", 0, 0, 10, 20))
        building = self._buildings.get_building(1)
        self.assertIsNotNone(building)

        if building is not None:
            self.assertEqual(building["name"], "Tower")

    def test_get_all_buildings(self) -> None:
        self._buildings.add_building("A", 0, 0, 1, 1)
        self._buildings.add_building("B", 1, 1, 2, 2)
        all_buildings = self._buildings.get_all_buildings()
        self.assertEqual(len(all_buildings), 2)

    def test_add_duplicate_building(self) -> None:
        self._buildings.add_building("Wall", 0, 0, 5, 5)
        result = self._buildings.add_building("Wall", 1, 1, 2, 2)
        self.assertFalse(result)

    def test_delete_building(self) -> None:
        self._buildings.add_building("Outpost", 0, 0, 4, 4)
        self.assertTrue(self._buildings.delete_building(1))
        self.assertIsNone(self._buildings.get_building(1))

    def test_add_and_get_monster_type(self) -> None:
        self.assertTrue(self._monster_types.add_monster_type("Goblin", 50, 10, 5))
        monster = self._monster_types.get_monster_type(1)
        self.assertIsNotNone(monster)

        if monster is not None:
            self.assertEqual(monster["base_attack"], 10)

    def test_get_all_monster_types(self) -> None:
        self._monster_types.add_monster_type("Wolf", 60, 12, 4)
        self._monster_types.add_monster_type("Bear", 120, 20, 10)
        all_monsters = self._monster_types.get_all_monster_types()
        self.assertEqual(len(all_monsters), 2)

    def test_delete_monster_type(self) -> None:
        self._monster_types.add_monster_type("Troll", 80, 15, 8)
        self.assertTrue(self._monster_types.delete_monster_type(1))
        self.assertIsNone(self._monster_types.get_monster_type(1))

    def test_add_and_get_item(self) -> None:
        self.assertTrue(self._items.add_item("Potion", "Heal 50 HP"))
        item = self._items.get_item(1)

        if item is not None:
            self.assertEqual(item["effect"], "Heal 50 HP")

    def test_get_all_items(self) -> None:
        self._items.add_item("Elixir", "Restore mana")
        self._items.add_item("Scroll", "Fireball spell")
        all_items = self._items.get_all_items()
        self.assertEqual(len(all_items), 2)

    def test_delete_item(self) -> None:
        self._items.add_item("Amulet", "Increases defense")
        self.assertTrue(self._items.delete_item(1))
        self.assertIsNone(self._items.get_item(1))

    def test_add_duplicate_item(self) -> None:
        self._items.add_item("Ring", "Magic boost")
        self.assertFalse(self._items.add_item("Ring", "Magic boost"))

    def test_add_and_get_spawn_point(self) -> None:
        self._buildings.add_building("Fort", 5, 5, 15, 15)
        self.assertTrue(self._spawn_points.add_spawn_point(1, 1.0, 1.0, 0.5))
        spawn_point = self._spawn_points.get_spawn_point(1)

        if spawn_point is not None:
            self.assertAlmostEqual(spawn_point["spawn_rate"], 0.5)

    def test_get_all_spawn_points(self) -> None:
        self._buildings.add_building("Keep", 0, 0, 10, 10)
        self._spawn_points.add_spawn_point(1, 0.5, 0.5, 0.2)
        self._spawn_points.add_spawn_point(1, 1.0, 1.0, 0.4)
        all_points = self._spawn_points.get_all_spawn_points()
        self.assertEqual(len(all_points), 2)

    def test_delete_spawn_point(self) -> None:
        self._buildings.add_building("Ruins", 0, 0, 2, 2)
        self._spawn_points.add_spawn_point(1, 2.0, 2.0, 0.3)
        self.assertTrue(self._spawn_points.delete_spawn_point(1))
        self.assertIsNone(self._spawn_points.get_spawn_point(1))

    def tearDown(self) -> None:
        self._connection.close()

if __name__ == "__main__":
    unittest.main()
