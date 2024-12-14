from typing import List

from fastapi import APIRouter

from api.dependencies import UnitOfWorkDependency, CurrentUserDependency
from schemas.trip import TripSchemaCreate, TripSchema, TripSchemaFind
from services.trips import TripsService

router = APIRouter(prefix="/trips")


@router.post("/")
async def create(uow: UnitOfWorkDependency, user: CurrentUserDependency, trip: TripSchemaCreate) -> TripSchema:
    """Creates a new trip from the car and a route."""
    return await TripsService.create(uow, user.id, trip)


@router.post("/find")
async def find(uow: UnitOfWorkDependency, user: CurrentUserDependency, filters: TripSchemaFind) -> List[TripSchema]:
    """Finish a trip by its ID, may be invoked only by the user who has created the trip"""
    return await TripsService.find(uow, user.id, filters)


@router.get("/{id}")
async def read(uow: UnitOfWorkDependency, user: CurrentUserDependency, id: int) -> TripSchema:
    """Reads a trip by its ID, may be invoked only by the user who has created the trip"""
    return await TripsService.read(uow, user.id, id)


@router.post("/{id}/finish")
async def finish(uow: UnitOfWorkDependency, user: CurrentUserDependency, id: int) -> TripSchema:
    """Finish a trip by its ID, may be invoked only by the user who has created the trip"""
    return await TripsService.finish(uow, user.id, id)
