from fastapi import APIRouter
from app.controllers.booking_controller import router as booking_controller

router = APIRouter()
router.include_router(booking_controller)
