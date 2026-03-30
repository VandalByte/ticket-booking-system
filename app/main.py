from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.database import connect_to_mongo, close_mongo_connection
from app.api.routes.auth import router as auth_router
from app.api.routes.events import router as event_router
from app.api.routes.seats import router as seat_router
from app.api.routes.bookings import router as booking_router
from app.api.routes.payments import router as payment_router
from dotenv import load_dotenv

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()


app = FastAPI(title="Ticket Booking API", lifespan=lifespan)

# Include API routers
app.include_router(auth_router)
app.include_router(event_router)
app.include_router(seat_router)
app.include_router(booking_router)
app.include_router(payment_router)

@app.get("/")
async def root():
    return {"message": "API is running"}
