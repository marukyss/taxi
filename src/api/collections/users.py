from fastapi import APIRouter

from api.dependencies import UnitOfWorkDependency, CurrentUserDependency
from schemas.user import UserSchemaCreate, UserSchema, UserSchemaLogin
from services.users import UsersService

router = APIRouter(prefix="/users")


@router.post("/")
async def create(request: UserSchemaCreate, uow: UnitOfWorkDependency) -> UserSchema:
    # Create a new user
    return await UsersService.create(uow, request)


@router.post("/login")
async def me(uow: UnitOfWorkDependency, credentials: UserSchemaLogin) -> UserSchema:
    # Login the user into the system, fails if the credentials are wrong
    return await UsersService.login(uow, credentials)


@router.get("/me")
async def me(user: CurrentUserDependency) -> UserSchema:
    # Return the current user to the client, fails if the client is not authenticated
    return user
