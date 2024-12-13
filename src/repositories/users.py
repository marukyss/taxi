from models.user import User
from repositories.base.sql import SqlRepository


class UsersRepository(SqlRepository[User]):
    __model__ = User
