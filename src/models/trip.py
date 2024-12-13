from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db.base_model import BaseSqlModel
from models.car import Car
from models.route import Route
from models.user import User


class Trip(BaseSqlModel):
    __tablename__ = "trips"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    car_id: Mapped[int] = mapped_column(ForeignKey(Car.id))
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id))
    route_id: Mapped[int] = mapped_column(ForeignKey(Route.id))

    started_at: Mapped[datetime]
    finished_at: Mapped[datetime] = mapped_column(nullable=True)
