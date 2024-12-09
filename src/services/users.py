import random
from hashlib import sha256

from models.user import User
from schemas.user import UserSchemaCreate, UserSchema
from utils.exceptions import UserAlreadyExistsError, UserNotFoundError
from utils.schema import from_sql_model
from utils.uow import UnitOfWorkFactory


class UsersService:
    @staticmethod
    async def create(uow: UnitOfWorkFactory, user: UserSchemaCreate) -> UserSchema:
        async with uow() as transaction:
            if len(await transaction.users.find(username=user.username)) > 0:
                raise UserAlreadyExistsError(f"The <User username={user.username}> already exists")

            model = await transaction.users.create(User(
                username=user.username,
                password_hash=sha256(user.password.encode('utf-8')).hexdigest(),
                token=UsersService.__generate_user_token(user.password),
                balance=1000,
                committed_trips=0
            ))

            await transaction.commit()

        return from_sql_model(model, UserSchema)

    @staticmethod
    async def find_by_token(uow: UnitOfWorkFactory, token: str) -> UserSchema | None:
        async with uow() as transaction:
            authorized = await transaction.users.find(token=token)

        if len(authorized) == 0:
            return None

        return from_sql_model(authorized[0], UserSchema)

    @staticmethod
    async def read(uow: UnitOfWorkFactory, id: int) -> UserSchema:
        async with uow() as transaction:
            resolved = await transaction.users.find(id=id)

            if len(resolved) == 0:
                raise UserNotFoundError(f"The <User id={id}> cannot be found")

        return from_sql_model(resolved[0], UserSchema)

    @staticmethod
    def __generate_user_token(password: str) -> str:
        hash = sha256(password.encode("utf-8")).hexdigest()
        return ''.join(random.choices(hash, k=32))
