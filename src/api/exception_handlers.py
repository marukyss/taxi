from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from utils.exceptions import *


def handle_service_error(_: Request, exc: ServiceError) -> JSONResponse:
    # Compare exceptions to their http statuses
    statuses = {
        'user_already_exists': status.HTTP_400_BAD_REQUEST,
        'user_not_found': status.HTTP_404_NOT_FOUND,
        'user_credentials_invalid': status.HTTP_400_BAD_REQUEST,
        'route_not_found': status.HTTP_404_NOT_FOUND,
        'car_not_found': status.HTTP_404_NOT_FOUND,
        'trip_not_found': status.HTTP_404_NOT_FOUND
    }

    code = statuses.get(exc.type, status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Send the exception to the client
    return JSONResponse(
        status_code=code,
        content={
            "type": exc.type,
            "message": exc.message
        }
    )


def handle_http_exception(_: Request, exc: HTTPException):
    # Compare http statuses to their text representations
    types = {
        status.HTTP_401_UNAUTHORIZED: "unauthorized",
        status.HTTP_404_NOT_FOUND: "not_found",
        status.HTTP_405_METHOD_NOT_ALLOWED: "method_not_allowed"
    }

    type = types.get(exc.status_code, "unknown")

    # Send the response
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "type": type,
            "message": exc.detail
        }
    )


def handle_validation_error(_: Request, exc: RequestValidationError):
    # Rebuild an exception body in more fancy manner
    entries = []

    for error in exc.args[0]:
        entries.append({
            "type": error["msg"],
            "field": '/'.join(error["loc"]),
            "input": error["input"]
        })

    # Send the response with the newly created body
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "type": "bad_request",
            "message": entries
        }
    )


def handle_not_found(req: Request, _: Exception) -> JSONResponse:
    # Reuse existing HTTP-Exception handler to send the actual response
    return handle_http_exception(req, HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"The page '{req.url}' was not found on this server"
    ))


def handle_method_not_allowed(req: Request, _: Exception) -> JSONResponse:
    # Reuse existing HTTP-Exception handler to send the actual response
    return handle_http_exception(req, HTTPException(
        status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
        detail=f"The method '{req.method}' is not allowed for '{req.url}'"
    ))
