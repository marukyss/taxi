from typing import List

from schemas.car import CarSchema, CarSchemaFind
from utils.exceptions import CarNotFoundError
from utils.schema import from_sql_model
from utils.uow import UnitOfWorkFactory


class CarsService:
    @staticmethod
    async def find(uow: UnitOfWorkFactory, query: CarSchemaFind) -> List[CarSchema]:
        async with uow() as transaction:
            models = await transaction.cars.find(
                driver_smokes=not query.smokeless,
                supports_children=query.allows_children,
                supports_disabled=query.allows_disabled,
                supports_luggage=query.allows_luggage,
                supports_animals=query.allows_animals
            )

        filtered_by_price = filter(
            lambda car: car.price_per_kilometer*query.required_distance <= query.max_price,
            models
        )

        return [from_sql_model(model, CarSchema) for model in filtered_by_price]

    @staticmethod
    async def read(uow: UnitOfWorkFactory, id: int) -> CarSchema:
        async with uow() as transaction:
            models = await transaction.cars.find(id=id)
            if len(models) == 0:
                raise CarNotFoundError(f"The <Car id={id}> was not found")

        return from_sql_model(models[0], CarSchema)
