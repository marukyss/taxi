import hashlib

from models.route import Route
from schemas.route import RouteSchema, RouteSchemaCreate
from utils.exceptions import RouteNotFoundError
from utils.schema import from_sql_model
from utils.uow import UnitOfWorkFactory


class RoutesService:
    @staticmethod
    async def create(uow: UnitOfWorkFactory, route: RouteSchemaCreate) -> RouteSchema:
        async with uow() as transaction:
            distance = await RoutesService.__estimate_distance_kilometers(route.start_address, route.end_address)
            time = await RoutesService.__estimate_mean_time_minutes(route.start_address, route.end_address)

            model = await transaction.routes.create(Route(
                start_address=route.start_address,
                end_address=route.end_address,
                distance_kilometers=distance,
                mean_time_minutes=time
            ))

            await transaction.commit()

        return from_sql_model(model, RouteSchema)

    @staticmethod
    async def refresh(uow: UnitOfWorkFactory, id: int) -> RouteSchema:
        async with uow() as transaction:
            existing = await transaction.routes.find(id=id)
            if len(existing) == 0:
                raise RouteNotFoundError(f"The <Route id={id}> was not found")

            found = existing[0]

            distance = await RoutesService.__estimate_distance_kilometers(found.start_address, found.end_address)
            time = await RoutesService.__estimate_mean_time_minutes(found.start_address, found.end_address)

            updated = Route(
                id=found.id,
                start_address=found.start_address,
                end_address=found.end_address,
                distance_kilometers=distance,
                mean_time_minutes=time
            )

            await transaction.routes.update(updated)
            await transaction.commit()

        return from_sql_model(updated, RouteSchema)

    @staticmethod
    async def read(uow: UnitOfWorkFactory, id: int) -> RouteSchema:
        async with uow() as transaction:
            existing = await transaction.routes.find(id=id)
            if len(existing) == 0:
                raise RouteNotFoundError(f"The <Route id={id}> was not found")

        return from_sql_model(existing[0], RouteSchema)

    @staticmethod
    async def __estimate_distance_kilometers(start_address: str, end_address: str) -> float:
        # Here should be a complex service, but for demonstration purposes...
        hash1 = int(hashlib.md5(start_address.encode('utf-8')).hexdigest(), 16)
        hash2 = int(hashlib.md5(end_address.encode('utf-8')).hexdigest(), 16)
        diff = hash2 - hash1

        return round(abs(diff % 1000)/1000, 3)

    @staticmethod
    async def __estimate_mean_time_minutes(start_address: str, end_address: str) -> float:
        # Here should be a complex service, but for demonstration purposes...
        precise = await RoutesService.__estimate_distance_kilometers(start_address, end_address)*1.2
        return round(precise, 5)
