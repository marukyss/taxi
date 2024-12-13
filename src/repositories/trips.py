from models.trip import Trip
from repositories.base.sql import SqlRepository


class TripsRepository(SqlRepository[Trip]):
    __model__ = Trip
