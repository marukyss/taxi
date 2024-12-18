from db.engine import SqlEngine


class SqlDbProvider:
    """Singleton provider for the service SqlEngine instance."""

    __sql_engine: SqlEngine | None = None

    @staticmethod
    def init(url: str) -> None:
        """Initializes the underlying DbEngine instance.
        Should be invoked before the instance is accessed.
        May throw the same exceptions as SqlEngine constructor
        """

        SqlDbProvider.__sql_engine = SqlEngine(url)

    @staticmethod
    def engine() -> SqlEngine:
        """Returns the engine instance contained in this singleton."""

        if SqlDbProvider.__sql_engine is None:
            raise AssertionError("The DB provider was not initialized")

        return SqlDbProvider.__sql_engine
