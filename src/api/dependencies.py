from typing import Annotated

from fastapi import Depends, Header, HTTPException
from starlette import status

from db.provider import SqlDbProvider
from schemas.user import UserSchema
from services.users import UsersService
from utils.uow import UnitOfWorkFactory


def unit_of_work() -> UnitOfWorkFactory:
    # Expose the SqlDb singleton to the endpoints
    return UnitOfWorkFactory(SqlDbProvider.engine().session_maker())


UnitOfWorkDependency = Annotated[UnitOfWorkFactory, Depends(unit_of_work)]


async def current_user(authentication: Annotated[str, Header()], uow: UnitOfWorkDependency) -> UserSchema:
    # Find the current user by authentication token attached to the request
    user = await UsersService.find_by_token(uow, authentication)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"The token '{authentication}' is not owned by any user"
        )

    return user

CurrentUserDependency = Annotated[UserSchema, Depends(current_user)]
