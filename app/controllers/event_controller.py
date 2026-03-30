from fastapi import APIRouter, Depends, status
from app.core.database import get_db
from app.repositories.event_repository import EventRepository
from app.repositories.seat_repository import SeatRepository
from app.services.event_service import EventService
from app.schemas.event_schema import EventCreateRequest, EventResponse
from app.core.dependencies import check_role

router = APIRouter(prefix="/events", tags=["Events"])


def get_event_service(db=Depends(get_db)):
    event_repo = EventRepository(db)
    seat_repo = SeatRepository(db)
    return EventService(event_repo, seat_repo)


@router.post("/", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
async def create_event(
    event_data: EventCreateRequest,
    service: EventService = Depends(get_event_service),
    current_user=Depends(check_role("organizer")),
):
    return await service.create_event_with_seats(event_data, current_user.user_id)


@router.get("/", response_model=list[EventResponse])
async def list_events(db=Depends(get_db)):
    repo = EventRepository(db)
    return await repo.get_all_events()
