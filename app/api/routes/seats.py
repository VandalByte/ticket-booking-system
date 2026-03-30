from fastapi import APIRouter
from app.controllers.seat_controller import router as seat_controller

router = APIRouter()
router.include_router(seat_controller)
