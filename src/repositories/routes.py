from models.route import Route
from repositories.base.sql import SqlRepository


class RoutesRepository(SqlRepository[Route]):
    __model__ = Route
