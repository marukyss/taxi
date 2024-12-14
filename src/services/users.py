import random
from hashlib import sha256

from models.user import User
from schemas.user import UserSchemaCreate, UserSchema, UserSchemaLogin
from utils.exceptions import UserAlreadyExistsError, UserNotFoundError, UserCredentialsInvalidError, \
    UserBalanceTooLowError
from utils.schema import from_sql_model
from utils.uow import UnitOfWorkFactory


class UsersService:
    """The business logic for the user management."""

    @staticmethod
    async def create(uow: UnitOfWorkFactory, user: UserSchemaCreate) -> UserSchema:
        """Creates a new user.
        Requires unique username. Does not validate the password strength.
        """

        async with uow() as transaction:
            if len(await transaction.users.find(username=user.username)) > 0:
                raise UserAlreadyExistsError(f"The <User username={user.username}> already exists")

            model = await transaction.users.create(User(
                username=user.username,
                password_hash=UsersService.__generate_password_hash(user.password),
                token=UsersService.__generate_user_token(user.password),
                balance=1000,
                committed_trips=0
            ))

            await transaction.commit()

        return from_sql_model(model, UserSchema)

    @staticmethod
    async def login(uow: UnitOfWorkFactory, credentials: UserSchemaLogin) -> UserSchema:
        """Authorizes the user by the given credentials.
        Throws UserInvalidCredentialsError if the username/password combination is invalid.
        """

        password_hash = UsersService.__generate_password_hash(credentials.password)

        async with uow() as transaction:
            resolved = await transaction.users.find(username=credentials.username, password_hash=password_hash)

        if len(resolved) == 0:
            raise UserCredentialsInvalidError(f"The <User username={credentials.username} password={credentials.password}> does not exist")

        return from_sql_model(resolved[0], UserSchema)

    @staticmethod
    async def charge_money(uow: UnitOfWorkFactory, id: int, value: float) -> UserSchema:
        """Charges money from the user's account.
        Fails if the user does not have enough money, or it simply does not exist
        """

        async with uow() as transaction:
            resolved = await transaction.users.find(id=id)

            if len(resolved) == 0:
                raise UserNotFoundError(f"The <User id={id}> does not exist")

            if resolved[0].balance < value:
                raise UserBalanceTooLowError(f"The <User id={id}> balance is too low to charge {value} conventional units")

            resolved[0].balance -= value

            await transaction.users.update(resolved[0])
            await transaction.commit()

        return from_sql_model(resolved[0], UserSchema)

    @staticmethod
    async def read(uow: UnitOfWorkFactory, id: int) -> UserSchema:
        """Returns the user with the given id.
        Throws UserNotFoundError if the user does not exist.
        """

        async with uow() as transaction:
            resolved = await transaction.users.find(id=id)

            if len(resolved) == 0:
                raise UserNotFoundError(f"The <User id={id}> does not exist")

        return from_sql_model(resolved[0], UserSchema)

    @staticmethod
    async def find_by_token(uow: UnitOfWorkFactory, token: str) -> UserSchema | None:
        """Tries to find a user by its token.
        If nothing was found returns None.
        """

        async with uow() as transaction:
            authorized = await transaction.users.find(token=token)

        if len(authorized) == 0:
            return None

        return from_sql_model(authorized[0], UserSchema)

    @staticmethod
    def __generate_user_token(password: str) -> str:
        chars_pool = UsersService.__generate_password_hash(password)
        return ''.join(random.choices(chars_pool, k=32))

    @staticmethod
    def __generate_password_hash(password: str) -> str:
        return sha256(password.encode("utf-8")).hexdigest()
