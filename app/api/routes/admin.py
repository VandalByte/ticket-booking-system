from fastapi import APIRouter
from app.controllers.admin_controller import router as admin_controller

router = APIRouter()
router.include_router(admin_controller)
