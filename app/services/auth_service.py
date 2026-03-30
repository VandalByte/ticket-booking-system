from app.repositories.user_repository import UserRepository
from app.core.security import hash_password, verify_password, create_access_token
from app.schemas.auth_schema import RegisterRequest, LoginRequest, TokenResponse
from fastapi import HTTPException, status


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def register_user(self, user_data: RegisterRequest):
        # Check if user already exists
        existing_user = await self.user_repo.get_user_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        hashed = hash_password(user_data.password)  # hash password

        return await self.user_repo.create_user(user_data, hashed)

    async def login_user_credentials(self, email: str, password: str) -> TokenResponse:
        user = await self.user_repo.get_user_by_email(email)  # Find user
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Verify password
        if not verify_password(password, user["password"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Create Token
        token = create_access_token(subject=user["_id"], role=user["role"])

        return TokenResponse(access_token=token, token_type="bearer")
