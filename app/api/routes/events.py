from fastapi import APIRouter
from app.controllers.event_controller import router as event_controller

router = APIRouter()
router.include_router(event_controller)
