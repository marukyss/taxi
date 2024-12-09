from pydantic import BaseModel


class UserSchema(BaseModel):
    """The user representation.

    Attributes
    ----------
    id : int
        The unique id of the user.
    username : str
        The unique username of the user.
    token : str
        The current authentication token of the user.
    balance : int
        The remaining balance of the user.
    committed_trips : int
        THe number of trips ridden by this user since the account creation.
    """

    id: int

    username: str
    token: str

    balance: float
    committed_trips: int


class UserSchemaCreate(BaseModel):
    """The user registration representation.

    Attributes
    ----------
    username : str
        The username of the new user.
        Should be unique.
    password : str
        The password of the new user.
    """

    username: str
    password: str


class UserSchemaLogin(BaseModel):
    """The user login credentials representation.

    Attributes
    ----------
    username : str
        The username of the targeted user.
    password : str
        The password of the targeted user.
    """

    username: str
    password: str
