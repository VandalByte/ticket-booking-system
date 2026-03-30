from fastapi import APIRouter, Depends
from app.core.database import get_db, get_redis
from app.repositories.seat_repository import SeatRepository
from app.services.seat_service import SeatService
from app.schemas.seat_schema import SeatLockRequest, SeatResponse
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/seats", tags=["Seats"])


def get_seat_service(db=Depends(get_db), redis=Depends(get_redis)):
    repo = SeatRepository(db)
    return SeatService(repo, redis)


@router.post("/lock")
async def lock_seats(
    payload: SeatLockRequest,
    service: SeatService = Depends(get_seat_service),
    current_user=Depends(get_current_user),
):
    return await service.lock_seats(
        payload.event_id, payload.seat_numbers, current_user.user_id
    )
