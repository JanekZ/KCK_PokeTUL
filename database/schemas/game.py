import sqlite3

def define() -> None:
    ''' Creates a database schema for "game.db" '''

    # Establish connection to the database
    connection = sqlite3.connect("database/data/game.db")
    database = connection.cursor()

    # Define 'players' table
    database.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY NOT NULL UNIQUE,
            name TEXT NOT NULL,
            password TEXT NOT NULL,
            level INTEGER DEFAULT 1 NOT NULL,
            last_x REAL NOT NULL DEFAULT 0,
            last_y REAL NOT NULL DEFAULT 0,
            is_banned BOOLEAN DEFAULT 0 NOT NULL,
            created DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Define 'sessions' table
    database.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY UNIQUE,
            player_id INTEGER NOT NULL,
            created DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (player_id) REFERENCES players(id)
        )
    ''')

    # Define 'monsters' table
    database.execute('''
        CREATE TABLE IF NOT EXISTS monsters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER NOT NULL,
            type_id INTEGER NOT NULL,
            nickname TEXT,
            level INTEGER DEFAULT 1 NOT NULL,
            experience INTEGER DEFAULT 0 NOT NULL,
            in_party BOOLEAN DEFAULT 0 NOT NULL,
            FOREIGN KEY (player_id) REFERENCES players(id)
        )
    ''')

    # Define 'inventory' table
    database.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            player_id INTEGER NOT NULL,
            item_id INTEGER NOT NULL,
            quantity INTEGER DEFAULT 1 NOT NULL,
            PRIMARY KEY (player_id, item_id),
            FOREIGN KEY (player_id) REFERENCES players(id)
        )
    ''')

    # Define 'progress' table
    database.execute('''
        CREATE TABLE IF NOT EXISTS progress (
            player_id INTEGER NOT NULL,
            building_id INTEGER NOT NULL,
            discovered BOOLEAN DEFAULT 0 NOT NULL,
            last_visited DATETIME,
            PRIMARY KEY (player_id, building_id),
            FOREIGN KEY (player_id) REFERENCES players(id)
        )
    ''')

    # Commit changes
    connection.commit()

    # Close the connection
    connection.close()

def delete() -> None:
    ''' Deletes a database schema for "game.db" '''

    # Establish connection to the database
    connection = sqlite3.connect("database/data/game.db")
    database = connection.cursor()

    # Drop every existing table in the database
    tables = ["players", "sessions", "monsters", "inventory", "progress"]

    for table in tables:
        database.execute(f"DROP TABLE IF EXISTS {table}")

    # Commit changes
    connection.commit()

    # Close the connection
    connection.close()
