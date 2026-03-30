from fastapi import APIRouter, Depends
from app.core.database import get_db, get_redis
from app.repositories.payment_repository import PaymentRepository
from app.repositories.booking_repository import BookingRepository
from app.repositories.seat_repository import SeatRepository
from app.services.payment_service import PaymentService
from app.schemas.payment_schema import PaymentCreateRequest, PaymentResponse
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/payments", tags=["Payments"])


def get_payment_service(db=Depends(get_db), redis=Depends(get_redis)):
    return PaymentService(
        payment_repo=PaymentRepository(db),
        booking_repo=BookingRepository(db),
        seat_repo=SeatRepository(db),
        redis_client=redis,
    )


@router.post("/confirm", response_model=PaymentResponse)
async def confirm_payment(
    payload: PaymentCreateRequest,
    service: PaymentService = Depends(get_payment_service),
    current_user=Depends(get_current_user),
):
    return await service.confirm_and_process(
        booking_id=payload.booking_id,
        user_id=current_user.user_id,
        method=payload.payment_method,
    )
