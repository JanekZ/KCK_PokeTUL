def save_session(session_id: str):
    with open("cookie.session", "w") as f:
        f.write(session_id)

def load_session() -> str | None:
    try:
        with open("cookie.session", "r") as f:
            session_id = f.read().strip()

            return session_id if session_id else None
    except FileNotFoundError:
        return None
