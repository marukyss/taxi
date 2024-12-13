from fastapi import APIRouter

from api.collections.users import router as users
from api.collections.cars import router as cars
from api.collections.routes import router as routes
#from api.trips import router as trips

router = APIRouter()

# Assemble all the application endpoint sets into the single one
router.include_router(users)
router.include_router(cars)
router.include_router(routes)
#router.include_router(trips)
