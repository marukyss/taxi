from fastapi import APIRouter

from api.dependencies import UnitOfWorkDependency, CurrentUserDependency
from schemas.route import RouteSchemaCreate, RouteSchema
from services.routes import RoutesService

router = APIRouter(prefix="/routes")


@router.post("/")
async def create(uow: UnitOfWorkDependency, _: CurrentUserDependency, request: RouteSchemaCreate) -> RouteSchema:
    """Creates a new route"""
    return await RoutesService.create(uow, request)


@router.get("/{id}")
async def read(uow: UnitOfWorkDependency, _: CurrentUserDependency, id: int) -> RouteSchema:
    """Reads the existing route, fails if the route does not exist"""
    return await RoutesService.read(uow, id)


@router.post("/{id}/refresh")
async def refresh(uow: UnitOfWorkDependency, _: CurrentUserDependency, id: int) -> RouteSchema:
    """Recalculates the existing route, fails if the route does not exist"""
    return await RoutesService.refresh(uow, id)
