from fastapi import APIRouter, Depends, HTTPException
from app.core.database import get_db, get_redis
from app.repositories.booking_repository import BookingRepository
from app.repositories.seat_repository import SeatRepository
from app.schemas.payment_schema import PaymentCreateRequest, PaymentResponse
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("/confirm")
async def confirm_payment(
    payload: PaymentCreateRequest,
    db=Depends(get_db),
    redis=Depends(get_redis),
    current_user=Depends(get_current_user),
):
    booking_repo = BookingRepository(db)
    seat_repo = SeatRepository(db)

    # Get the booking
    booking = await booking_repo.get_booking_by_id(payload.booking_id)
    if not booking or booking["user_id"] != current_user.user_id:
        raise HTTPException(status_code=404, detail="Booking not found")

    # Update Booking to Confirmed
    await booking_repo.update_status(payload.booking_id, "confirmed")

    # Mark Seats as 'booked' in MongoDB
    await seat_repo.mark_seats_booked(booking["event_id"], booking["seat_numbers"])

    # Clean up Redis (release the lock)
    for seat in booking["seat_numbers"]:
        redis.delete(f"lock:{booking['event_id']}:{seat}")

    return {
        "message": "Payment successful and seats confirmed!",
        "booking_id": payload.booking_id,
    }
