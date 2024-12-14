from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from db.provider import SqlDbProvider
from main import app
from models.car import Car, CarCategory
from models.route import Route
from models.trip import Trip
from models.user import User
from repositories.cars import CarsRepository
from repositories.routes import RoutesRepository
from repositories.trips import TripsRepository
from repositories.users import UsersRepository


async def reset_db():
    engine = SqlDbProvider.engine()

    await engine.drop_all()
    await engine.create_all()

    session: AsyncSession = engine.session_maker()()

    # Create dummy users
    users = UsersRepository(session)

    await users.create(User(
        id=1,
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
        model="Audi E8",
        driver_smokes=True,
        supports_children=True,
        supports_disabled=False,
        supports_luggage=True,
        supports_animals=True
    ))

    await cars.create(Car(
        id=2,
        category=CarCategory.Business,
        price_per_kilometer=2.5,
        model="BMW i3",
        driver_smokes=True,
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
        supports_luggage=True,
        supports_animals=False
    ))

    await cars.create(Car(
        id=4,
        category=CarCategory.Eco,
        price_per_kilometer=10.2,
        model="Kia Sport",
        driver_smokes=True,
        supports_children=True,
        supports_disabled=False,
        supports_luggage=True,
        supports_animals=False
    ))

    # Create the dummy route
    routes = RoutesRepository(session)

    await routes.create(Route(
        id=1,
        start_address="abc",
        end_address="xyz",
        distance_kilometers=10.123,
        mean_time_minutes=15.4
    ))

    # Create the dummy trips
    trips = TripsRepository(session)

    await trips.create(Trip(
        id=1,
        car_id=1,
        user_id=1,
        route_id=1,
        started_at="2024-12-14T00:00:00",
        finished_at="2024-12-14T00:10:00"
    ))

    await trips.create(Trip(
        id=2,
        car_id=2,
        user_id=1,
        route_id=1,
        started_at="2024-12-14T00:02:00",
        finished_at="2024-12-14T00:08:00"
    ))

    await session.commit()
    await session.close()

    await engine.dispose()


@asynccontextmanager
async def custom_lifespan(_: FastAPI):
    SqlDbProvider.init("mysql+aiomysql://taxi:SuperTaxi123!@3.77.96.62:3306/taxi-test")
    await reset_db()
    yield 
    

# Insert the custom lifespan    
app.router.lifespan_context = custom_lifespan
