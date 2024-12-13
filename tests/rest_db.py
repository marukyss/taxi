import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from models.car import Car, CarCategory
from models.user import User
from repositories.cars import CarsRepository
from repositories.users import UsersRepository
from repositories.routes import RoutesRepository
from repositories.trips import TripsRepository
from src.db.engine import SqlEngine


async def main():
    engine = SqlEngine("mysql+aiomysql://taxi:SuperTaxi123!@3.77.96.62:3306/taxi")

    await engine.drop_all()
    await engine.create_all()

    session: AsyncSession = engine.session_maker()()

    # Create dummy users
    users = UsersRepository(session)

    await users.create(User(
        id=999,
        username="u7i",
        password_hash="65e84be33532fb784c48129675f9eff3a682b27168c0ea744b2cf58ee02337c5",
        token="r86gmvwr0qoyjvl4spw9xtxo5civ629k",
        balance=1000,
        committed_trips=1
    ))

    # Create dummy cars
    cars = CarsRepository(session)

    await cars.create(Car(
        id=1,
        category=CarCategory.Cheap,
        price_per_kilometer=1.5,
        model="Audio E8",
        driver_smokes=True,
        supports_children=True,
        supports_disabled=False,
        supports_luggage=True,
        supports_animals=False
    ))

    await cars.create(Car(
        id=2,
        category=CarCategory.Business,
        price_per_kilometer=2.5,
        model="BMW i3",
        driver_smokes=False,
        supports_children=True,
        supports_disabled=False,
        supports_luggage=True,
        supports_animals=False
    ))

    await cars.create(Car(
        id=3,
        category=CarCategory.Eco,
        price_per_kilometer=4.2,
        model="BMW i7",
        driver_smokes=True,
        supports_children=True,
        supports_disabled=False,
        supports_luggage=False,
        supports_animals=False
    ))

    await session.commit()
    await session.close()

    await engine.dispose()

asyncio.run(main())
