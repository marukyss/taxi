from pydantic import BaseModel

from models.car import CarCategory


class CarSchema(BaseModel):
    id: int
    category: CarCategory
    price_per_kilometer: float
    model: str

    driver_smokes: bool
    supports_children: bool
    supports_disabled: bool
    supports_luggage: bool
    supports_animals: bool


class CarSchemaFind(BaseModel):
    required_distance: float
    max_price: float
    smokeless: bool
    allows_children: bool
    allows_disabled: bool
    allows_luggage: bool
    allows_animals: bool
