import sqlite3

def define() -> None:
    ''' Creates a database schema for "constants.db" '''

    # Establish connection to the database
    connection = sqlite3.connect("database/data/constants.db")
    database = connection.cursor()

    # Define 'buildings' table
    database.execute('''
        CREATE TABLE IF NOT EXISTS buildings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            x REAL NOT NULL,
            y REAL NOT NULL,
            width REAL NOT NULL,
            height REAL NOT NULL,
            color TEXT NOT NULL DEFAULT '#FFFFFF'
        )
    ''')

    # Define 'monster_types' table
    database.execute('''
        CREATE TABLE IF NOT EXISTS monster_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            base_health INTEGER NOT NULL,
            base_attack INTEGER NOT NULL,
            base_defense INTEGER NOT NULL
        )
    ''')

    # Define 'items' table
    database.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            effect TEXT NOT NULL
        )
    ''')

    # Define 'spawn_points' table
    database.execute('''
        CREATE TABLE IF NOT EXISTS spawn_points (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            building_id INTEGER NOT NULL,
            x REAL NOT NULL,
            y REAL NOT NULL,
            spawn_rate REAL NOT NULL,
            FOREIGN KEY (building_id) REFERENCES buildings(id)
        )
    ''')

    # Commit changes
    connection.commit()

    # Close the connection
    connection.close()

def delete() -> None:
    ''' Deletes a database schema for "constants.db" '''

    # Establish connection to the database
    connection = sqlite3.connect("database/data/constants.db")
    database = connection.cursor()

    # Drop every existing table in the database
    tables = ["buildings", "monster_types", "items", "spawn_points"]

    for table in tables:
        database.execute(f"DROP TABLE IF EXISTS {table}")

    # Commit changes
    connection.commit()

    # Close the connection
    connection.close()
