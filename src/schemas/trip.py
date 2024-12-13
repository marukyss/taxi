from datetime import datetime

from pydantic import BaseModel


class TripSchema(BaseModel):
    id: int
    car_id: int
    user_id: int
    route_id: int

    started_at: datetime
    finished_at: datetime | None


class TripSchemaCreate(BaseModel):
    route_id: int
    car_id: int


class TripSchemaFind(BaseModel):
    user_id: int
