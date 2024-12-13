import asyncio

from sqlalchemy import ForeignKeyConstraint, inspect
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine, AsyncConnection
from sqlalchemy.sql.ddl import DropConstraint, DropTable

from db.base_model import BaseSqlModel


class SqlEngine:
    """The wrapper over the SQL AsyncEngine and async_sessionmaker classes.
    Provides straightforward way to interact with the DB within the service.
    """

    def __init__(self, url: str):
        """Creates a new engine from the given URL.
        Should be invoked when a server needs to connect to another database.
        """

        self.__engine: AsyncEngine = create_async_engine(url)
        self.__session_maker: async_sessionmaker = async_sessionmaker(self.__engine, expire_on_commit=False)

    async def create_all(self) -> None:
        """Creates DB tables for all descendants of the BaseSqlModel.
        Creates ONLY if it is not yet presented in the DB.
        """

        async with self.__engine.begin() as conn:
            await conn.run_sync(BaseSqlModel.metadata.create_all)

    async def drop_all(self) -> None:
        """Deletes ALL the tables known to the application.
        Should be called with an EXTREME caution.
        """

        # Drop all the tables & the FK constraints
        async with self.__engine.begin() as conn:
            tables = []
            fk_constrains = []

            # Discover the DB structure
            for tbl in BaseSqlModel.metadata.tables.values():
                fk_list = await conn.run_sync(
                    lambda sync_conn: inspect(sync_conn).get_foreign_keys(tbl.name)
                )

                for fk in fk_list:
                    fk_constrains.append(ForeignKeyConstraint((), (), table=tbl, name=fk["name"]))

                tables.append(tbl)

            # Drop all the FK constrains at fist
            for fk in fk_constrains:
                await conn.execute(DropConstraint(fk))

            # Drop the tables freed from constrains
            for tbl in tables:
                await conn.execute(DropTable(tbl))

    def session_maker(self) -> async_sessionmaker:
        """Returns a session-maker for this DB engine."""
        return self.__session_maker

    async def dispose(self) -> None:
        """Terminates the engine should be invoked for before the application exits."""
        await self.__engine.dispose()
