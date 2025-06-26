import os

ENGINE_DIRECTORY = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def fix_path(path: str) -> str:
    return str(ENGINE_DIRECTORY + "/" + path)
