from pydantic import BaseModel


class RouteSchema(BaseModel):
    id: int

    start_address: str
    end_address: str

    distance_kilometers: float
    mean_time_minutes: float


class RouteSchemaCreate(BaseModel):
    start_address: str
    end_address: str
