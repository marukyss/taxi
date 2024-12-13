from enum import StrEnum

from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped

from db.base_model import BaseSqlModel


class CarCategory(StrEnum):
    Cheap = "cheap"
    Standard = "standard"
    Business = "business"
    Eco = "eco"


class Car(BaseSqlModel):
    __tablename__ = "cars"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    category: Mapped[CarCategory]
    price_per_kilometer: Mapped[float]
    model: Mapped[str] = mapped_column(String(256))

    driver_smokes: Mapped[bool]
    supports_children: Mapped[bool]
    supports_disabled: Mapped[bool]
    supports_luggage: Mapped[bool]
    supports_animals: Mapped[bool]
