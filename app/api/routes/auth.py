from fastapi import APIRouter
from app.controllers.auth_controller import router as auth_controller

router = APIRouter()
router.include_router(auth_controller)