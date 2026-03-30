from fastapi import APIRouter, Depends, status
from app.core.database import get_db
from app.repositories.user_repository import UserRepository
from fastapi.security import OAuth2PasswordRequestForm
from app.services.auth_service import AuthService
from app.schemas.auth_schema import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
)
from app.schemas.user_schema import UserResponse


router = APIRouter(prefix="/auth", tags=["Authentication"])


# Dependency to initialize the service
def get_auth_service(db=Depends(get_db)):
    repo = UserRepository(db)
    return AuthService(repo)


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register(
    user_data: RegisterRequest, service: AuthService = Depends(get_auth_service)
):
    """
    Creates a new user account.
    - Checks if email is unique
    - Hashes password via Argon2
    - Stores user in MongoDB
    """
    return await service.register_user(user_data)


@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    service: AuthService = Depends(get_auth_service)
):
    """
    Authenticate user and return a JWT token.
    Note: 'username' in form_data will be the user's email.
    """
    return await service.login_user_credentials(
        email=form_data.username, 
        password=form_data.password
    )
