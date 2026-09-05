class PlaygroundError(Exception):
    """Base error for the SQL playground."""


class QueryError(PlaygroundError):
    """Raised when SQLite rejects a statement the user typed."""
