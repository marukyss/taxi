from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from db.base_model import BaseSqlModel


class User(BaseSqlModel):
    """The user that operates within the system.

    Attributes
    ----------
    id : int
        The unique id of the user. Should not be changed during the user lifetime.
    username : str
        The unique username of the user. May be changed over the time.
        Used as additional secret during the authentication process.
    password_hash : str
        The SHA-256 hash of the user's password. Should not be exposed to the public API.
    token : str
        The static token that's used to authenticate the user.
        Should be regenerated when the password is changed.
    balance : int
        The current balance of the user, measured in the conventional units.
    committed_trips : int
        The number of trips that user took since the creation of the account.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    username: Mapped[str] = mapped_column(String(256))
    password_hash: Mapped[str] = mapped_column(String(256))
    token: Mapped[str] = mapped_column(String(64))

    balance: Mapped[float]
    committed_trips: Mapped[int]
