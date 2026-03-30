from fastapi import APIRouter
from app.controllers.user_controller import router as user_controller

router = APIRouter()
router.include_router(user_controller)
