from fastapi import APIRouter
from app.controllers.payment_controller import router as payment_controller

router = APIRouter()
router.include_router(payment_controller)
