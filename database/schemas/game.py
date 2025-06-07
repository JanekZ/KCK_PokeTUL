import sqlite3

def define() -> None:
    ''' Defines a new database schema '''

    # Establish the connection to the 'game.db' database
    connection = sqlite3.connect("database/data/game.db")
    database = connection.cursor()

    # Define the 'game.db' database schema
    database.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY NOT NULL UNIQUE,
            name TEXT NOT NULL,
            password TEXT NOT NULL,
            level INTEGER DEFAULT 1 NOT NULL,
            last_position TEXT,
            is_banned INTEGER DEFAULT 0 NOT NULL,
            unlocked_buildings TEXT,
            created DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    database.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY UNIQUE,
            FOREIGN KEY (player) REFERENCES players(id) NOT NULL
        )
    ''')

    database.execute('''
        CREATE TABLE IF NOT EXISTS monsters (
            id INTEGER PRIMRAY KEY AUTOINCREMENT UNIQUE,
            name TEXT NOT NULL,
            level INTEGER DEFAULT 1 NOT NULL,
            FOREIGN KEY (player) REFERENCES players(id) NOT NULL
        )
    ''')

    # Close the active connection
    connection.close()

def delete() -> None:
    ''' Deletes the database schema '''

    # Establish the connection to the 'game.db' database
    connection = sqlite3.connect("database/data/game.db")
    database = connection.cursor()

    # Define the 'game.db' database schema
    database.execute('''
        DROP TABLE IF EXISTS players
    ''')

    database.execute('''
        DROP TABLE IF EXISTS sessions
    ''')

    database.execute('''
        DROP TABLE IF EXISTS monsters
    ''')

    # Close the active connection
    connection.close()
