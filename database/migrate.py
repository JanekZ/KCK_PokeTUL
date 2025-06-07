import schemas.game
import schemas.constants

# Define the specified database schema
def run_migrate(schema) -> None:
    try:
        schema.delete()
    except:
        print(f"Could not delete '{str(schema)}'")

    try:
        schema.define()
    except:
        print(f"Could not define '{str(schema)}'")

# Migrate all available schemas
if __name__ == "__main__":
    run_migrate(schemas.game)
    run_migrate(schemas.constants)
