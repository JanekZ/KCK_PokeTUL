import sqlite3

def define() -> None:
    ''' Defines a new database schema '''

    # Establish the connection to the 'constants.db' database
    connection = sqlite3.connect("database/data/constants.db")
    database = connection.cursor()

    # Define the 'constants.db' database schema
    database.execute('''
        CREATE TABLE IF NOT EXISTS objects (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            layer TEXT NOT NULL,
            x_position INTEGER NOT NULL,
            y_position INTEGER NOT NULL,
            width INTEGER NOT NULL,
            height INTEGER NOT NULL,
            red INTEGER NOT NULL,
            green INTEGER NOT NULL,
            blue INTEGER NOT NULL,
            destination TEXT
        )
    ''')

    database.execute('''
        CREATE TABLE IF NOT EXISTS enities (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            type TEXT NOT NULL,
            x_position INTEGER NOT NULL,
            y_position INTEGER NOT NULL
        )
    ''')

    # Close the active connection
    connection.close()

def delete() -> None:
    ''' Deletes the database schema '''

    # Establish the connection to the 'constants.db' database
    connection = sqlite3.connect("database/data/constants.db")
    database = connection.cursor()

    # Define the 'constants.db' database schema
    database.execute('''
        DROP TABLE IF EXISTS objects
    ''')

    database.execute('''
        DROP TABLE IF EXISTS entities
    ''')

    # Close the active connection
    connection.close()
