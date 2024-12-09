from models.user import User
from repositories.base.sql import SqlRepository


class UsersRepository(SqlRepository):
    __model__ = User
