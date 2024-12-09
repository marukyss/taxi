class ServiceError(Exception):
    """Base class for all the errors emitted by business-logic.

    Class Attributes
    ----------------
    type : str
        The machine-readable category of this error.

    Methods
    -------
    constructor(message: str)
         Creates a new exception and sets a context-based description of an error
    """

    type: str = None

    def __init__(self, message: str):
        self.message: str = message

    def __str__(self) -> str:
        return f"<{self.type} message={self.message}>"


class UserAlreadyExistsError(ServiceError):
    type: str = "user_already_exists"


class UserNotFoundError(ServiceError):
    type: str = "user_not_found"


class RouteNotFoundError(ServiceError):
    type: str = "route_not_found"


class CarNotFoundError(ServiceError):
    type: str = "car_not_found"


class TripNotFoundError(ServiceError):
    type: str = "trip_not_found"
