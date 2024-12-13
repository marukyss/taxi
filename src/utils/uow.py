from typing import Self

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from repositories.cars import CarsRepository
from repositories.routes import RoutesRepository
from repositories.trips import TripsRepository
from repositories.users import UsersRepository


# TODO: Add comments (Mariia Hudz)
class UnitOfWork:
    def __init__(self, session: AsyncSession):
        self.__session: AsyncSession = session

        self.cars: CarsRepository = CarsRepository(self.__session)
        self.routes: RoutesRepository = RoutesRepository(self.__session)
        self.trips: TripsRepository = TripsRepository(self.__session)
        self.users: UsersRepository = UsersRepository(self.__session)

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.rollback()
        await self.__session.close()

    async def commit(self) -> None:
        await self.__session.commit()

    async def rollback(self) -> None:
        await self.__session.rollback()


# TODO: Add comments (Mariia Hudz)
class UnitOfWorkFactory:
    def __init__(self, session_factory: async_sessionmaker):
        self.__session_factory: async_sessionmaker = session_factory

    def __call__(self, *args, **kwargs) -> UnitOfWork:
        return UnitOfWork(self.__session_factory())
