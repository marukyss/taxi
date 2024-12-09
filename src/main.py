from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.middleware.cors import CORSMiddleware

from api.exception_handlers import handle_service_error, handle_http_exception, handle_validation_error, \
    handle_not_found, handle_method_not_allowed
from db.provider import SqlDbProvider
from api.router import router
from utils.exceptions import ServiceError


@asynccontextmanager
async def lifespan(_: FastAPI):
    # A function that is invoked on the startup of the service
    SqlDbProvider.init("mysql+aiomysql://taxi:SuperTaxi123!@3.77.96.62:3306/taxi")
    await SqlDbProvider.engine().create_all()
    yield


# Create the FastAPI application with only Swagger docs available
app = FastAPI(
    redoc_url=None,
    lifespan=lifespan
)

# Wrap all kinds of the expected errors into the corresponding wrappers
app.add_exception_handler(ServiceError, handle_service_error)
app.add_exception_handler(HTTPException, handle_http_exception)
app.add_exception_handler(RequestValidationError, handle_validation_error)
app.add_exception_handler(status.HTTP_404_NOT_FOUND, handle_not_found)
app.add_exception_handler(status.HTTP_405_METHOD_NOT_ALLOWED, handle_method_not_allowed)

# Add the support for CORS requests to make API accessible from different origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the service API
app.include_router(router)
