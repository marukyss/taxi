from typing import List, Type, Any

from sqlalchemy import select, update, delete, insert, Executable, literal_column, Result, Row
from sqlalchemy.exc import DataError, ProgrammingError, DatabaseError
from sqlalchemy.ext.asyncio import AsyncSession

from utils.model import to_dict


class SqlRepository[Model]:
    """Basic SQL CRUD repository.

    Static Attributes
    ----------
    __model__ : Type[Model]
        The type of the used model. MUST be redefined in concrete implementations.
        The primary key of the model MUST be called 'id'.
    """

    __model__: Type[Model] = None

    def __init__(self, session: AsyncSession):
        """Initializes the repository with the given session."""
        self.__session: AsyncSession = session

    async def create(self, model: Model) -> Model:
        """Adds a model to the table. May throw exceptions if the table couldn't be inserted correctly.
        Returns the created model with generated fields set (like id).
        """

        cls = self.__model__
        values = to_dict(model)

        # Build & invoke the query
        stmt = insert(cls).values(**values).returning(literal_column('*'))
        res = await self.__invoke_query_with_exceptions(stmt)

        # Extract the model from the row
        data = res.one()
        return cls(**{c.name: getattr(data, c.name) for c in cls.__table__.columns})

    async def update(self, model: Model) -> bool:
        """Updates the existing model in the table.
        Returns false if the model with the same id doesn't exist in the table.
        """

        cls = self.__model__
        values = to_dict(model)

        # Validate that the table contains the object in this transaction
        if len(await self.find(id=model.id)) == 0:
            return False

        # Build & invoke the query
        stmt = update(cls).values(**values).filter_by(id=model.id)
        await self.__invoke_query_with_exceptions(stmt)

        return True

    async def delete(self, id: int) -> bool:
        """Deletes the model existing in the table.
        Returns false if the model with the given id is not present in the table.
        """

        stmt = delete(self.__model__).filter_by(id=id).returning(self.__model__.id)
        res = await self.__invoke_query_with_exceptions(stmt)

        return res.scalar_one_or_none() is not None

    async def read_all(self, i: int, n: int) -> List[Model]:
        """Reads the models from the table.
        Shrinks the read range to [i; i + n]
        """

        # Build & invoke the query
        stmt = select(self.__model__).offset(i).limit(n)
        res = await self.__invoke_query_with_exceptions(stmt)

        # Extract & unbind objects from the query result
        results = [row[0] for row in res.all()]
        [self.__session.expunge(x) for x in results]
        return results

    async def find(self, **kwargs) -> List[Model]:
        """Finds the models from the table.
        Doesn't support paging.
        """

        # Build & invoke the query
        stmt = select(self.__model__).filter_by(**kwargs)
        res = await self.__invoke_query_with_exceptions(stmt)

        # Extract & unbind objects from the query result
        results = [row[0] for row in res.all()]
        [self.__session.expunge(x) for x in results]
        return results

    async def __invoke_query_with_exceptions(self, stmt: Executable) -> Result[Any]:
        try:
            return await self.__session.execute(stmt)
        except DataError as e:
            raise ValueError(str(e))
        except DatabaseError as e:
            raise IOError(str(e))
