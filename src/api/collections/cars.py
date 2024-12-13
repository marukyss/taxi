from typing import List

from fastapi import APIRouter

from api.dependencies import UnitOfWorkDependency
from schemas.car import CarSchemaFind, CarSchema
from services.cars import CarsService

router = APIRouter(prefix="/cars")


@router.post("/find")
async def find(uow: UnitOfWorkDependency, filters: CarSchemaFind) -> List[CarSchema]:
    """Finds a car based on a set of filters"""
    return await CarsService.find(uow, filters)
