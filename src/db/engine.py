import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine

from db.base_model import BaseSqlModel


class SqlEngine:
    """The wrapper over the SQL AsyncEngine and async_sessionmaker classes.
    Provides straightforward way to interact with the DB within the service.

    Methods
    -------
    constructor : (url: str)
        Create a new engine from the given URL. Should be invoked when a server needs to connect to another database.
    create_all : async () -> None:
        Creates DB tables for all descendants of the BaseSqlModel. Creates ONLY if it is not yet presented in the DB
    session_maker : () -> async_sessionmaker:
        Returns a session-maker for this DB engine.
    dispose : async () -> None
        Terminates the engine should be invoked for before the application exits.
    """

    def __init__(self, url: str):
        self.__engine: AsyncEngine = create_async_engine(url)
        self.__session_maker: async_sessionmaker = async_sessionmaker(self.__engine, expire_on_commit=False)

    async def create_all(self) -> None:
        async with self.__engine.begin() as conn:
            await conn.run_sync(BaseSqlModel.metadata.create_all)

    def session_maker(self) -> async_sessionmaker:
        return self.__session_maker

    async def dispose(self) -> None:
        await self.__engine.dispose()
