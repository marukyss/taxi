import datetime
from typing import List

from models.trip import Trip
from schemas.trip import TripSchemaFind, TripSchema, TripSchemaCreate
from services.cars import CarsService
from services.routes import RoutesService
from services.users import UsersService
from utils.exceptions import TripNotFoundError, TripAccessDeniedError, TripAlreadyFinishedError
from utils.schema import from_sql_model
from utils.uow import UnitOfWorkFactory


class TripsService:
    @staticmethod
    async def create(uow: UnitOfWorkFactory, user_id: int, trip: TripSchemaCreate) -> TripSchema:
        async with uow() as transaction:
            # Require dependencies (raises exceptions)
            await CarsService.read(uow, trip.car_id)
            await RoutesService.read(uow, trip.route_id)
            await UsersService.read(uow, user_id)

            # Insert the model
            model = await transaction.trips.create(Trip(
                car_id=trip.car_id,
                user_id=user_id,
                route_id=trip.route_id,
                started_at=datetime.datetime.now().replace(microsecond=0)
            ))

            await transaction.commit()

        return from_sql_model(model, TripSchema)

    @staticmethod
    async def finish(uow: UnitOfWorkFactory, user_id: int, id: int) -> TripSchema:
        async with uow() as transaction:
            models = await transaction.trips.find(id=id)

            if len(models) == 0:
                raise TripNotFoundError(f"The <Trip id={id}> was not found")

            if models[0].user_id != user_id:
                raise TripAccessDeniedError(f"The <User id={user_id}> have no access to the <Trip id={id}>")

            if models[0].finished_at is not None:
                raise TripAlreadyFinishedError(f"The <Trip id={id}> has already been finished")

            updated = Trip(
                id=models[0].id,
                car_id=models[0].car_id,
                user_id=models[0].user_id,
                route_id=models[0].route_id,
                started_at=models[0].started_at,
                finished_at=datetime.datetime.now().replace(microsecond=0)
            )

            await transaction.trips.update(updated)
            await transaction.commit()

        return from_sql_model(updated, TripSchema)

    @staticmethod
    async def find(uow: UnitOfWorkFactory, user_id: int, filters: TripSchemaFind) -> List[TripSchema]:
        async with uow() as transaction:
            models = await transaction.trips.find(**filters.model_dump(), user_id=user_id)

        return [from_sql_model(model, TripSchema) for model in models]

    @staticmethod
    async def read(uow: UnitOfWorkFactory, user_id: int, id: int) -> TripSchema:
        async with uow() as transaction:
            models = await transaction.trips.find(id=id)

        if len(models) == 0:
            raise TripNotFoundError(f"The <Trip id={id}> was not found")

        if models[0].user_id != user_id:
            raise TripAccessDeniedError(f"The <User id={user_id}> have no access to the <Trip id={id}>")

        return from_sql_model(models[0], TripSchema)
