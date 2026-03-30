from fastapi import APIRouter, Depends, status
from app.core.database import get_db, get_redis
from app.repositories.booking_repository import BookingRepository
from app.repositories.event_repository import EventRepository
from app.repositories.seat_repository import SeatRepository
from app.services.booking_service import BookingService
from app.schemas.booking_schema import BookingCreateRequest, BookingResponse
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/bookings", tags=["Bookings"])


def get_booking_service(db=Depends(get_db), redis=Depends(get_redis)):
    return BookingService(
        booking_repo=BookingRepository(db),
        event_repo=EventRepository(db),
        seat_repo=SeatRepository(db),
        redis_client=redis,
    )


@router.post("/", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
async def create_booking(
    payload: BookingCreateRequest,
    service: BookingService = Depends(get_booking_service),
    current_user=Depends(get_current_user),
):
    """
    Step 1: Verify the user owns the Redis lock for these seats.
    Step 2: Create a 'pending' booking in MongoDB.
    """
    return await service.initiate_booking(
        user_id=current_user.user_id,
        event_id=payload.event_id,
        seat_numbers=payload.seat_numbers,
    )
