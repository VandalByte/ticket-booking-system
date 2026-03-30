from fastapi import APIRouter
from app.api.routes import auth, users, events, seats, bookings, payments, admin

api_router = APIRouter()

api_router.include_router(
    auth.router,
    tags=["Auth"],
)

api_router.include_router(
    users.router,
    tags=["Users"],
)

api_router.include_router(
    events.router,
    tags=["Events"],
)

api_router.include_router(
    seats.router,
    tags=["Seats"],
)

api_router.include_router(
    bookings.router,
    tags=["Bookings"],
)

api_router.include_router(
    payments.router,
    tags=["Payments"],
)

api_router.include_router(
    admin.router,
    tags=["Admin"],
)
