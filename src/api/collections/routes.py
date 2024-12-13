from fastapi import APIRouter

from api.dependencies import UnitOfWorkDependency
from schemas.route import RouteSchemaCreate, RouteSchema
from services.routes import RoutesService

router = APIRouter(prefix="/routes")


@router.post("/")
async def create(request: RouteSchemaCreate, uow: UnitOfWorkDependency) -> RouteSchema:
    """Creates a new route"""
    return await RoutesService.create(uow, request)


@router.post("/{id}/refresh")
async def refresh(uow: UnitOfWorkDependency, id: int) -> RouteSchema:
    """Recalculates the existing route, fails if the route does not exist"""
    return await RoutesService.refresh(uow, id)
