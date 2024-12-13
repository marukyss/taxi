from models.car import Car
from repositories.base.sql import SqlRepository


class CarsRepository(SqlRepository[Car]):
    __model__ = Car
