from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from db.base_model import BaseSqlModel


class Route(BaseSqlModel):
    __tablename__ = "routes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    start_address: Mapped[str] = mapped_column(String(256))
    end_address: Mapped[str] = mapped_column(String(256))

    distance_kilometers: Mapped[float]
    mean_time_minutes: Mapped[float]
