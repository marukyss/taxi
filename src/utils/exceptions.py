class ServiceError(Exception):
    """Base class for all the errors emitted by business-logic.

    Static Attributes
    ----------------
    type : str
        The machine-readable category of this error.
    """

    type: str = None

    def __init__(self, message: str):
        """Creates a new exception and sets a context-based description of an error"""

        self.message: str = message

    def __str__(self) -> str:
        return f"<{self.type} message={self.message}>"


class UserAlreadyExistsError(ServiceError):
    type: str = "user_already_exists"


class UserNotFoundError(ServiceError):
    type: str = "user_not_found"


class UserCredentialsInvalidError(ServiceError):
    type: str = "user_credentials_invalid"


class UserBalanceTooLowError(ServiceError):
    type: str = "user_balance_too_low"


class RouteNotFoundError(ServiceError):
    type: str = "route_not_found"


class CarNotFoundError(ServiceError):
    type: str = "car_not_found"


class TripTooExpensiveError(ServiceError):
    type: str = "trip_too_expensive"


class TripNotFoundError(ServiceError):
    type: str = "trip_not_found"


class TripAccessDeniedError(ServiceError):
    type: str = "trip_access_denied"


class TripAlreadyFinishedError(ServiceError):
    type: str = "trip_already_finished"
