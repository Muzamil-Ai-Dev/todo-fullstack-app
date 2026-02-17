from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import Annotated
from src.database import get_session
from src.database.database import engine
from src.services.auth import AuthService
from src.schemas.user import UserLoginRequest, UserLoginResponse, UserRegisterRequest, UserRegisterResponse
from src.models.user import User, UserCreate
from src.utils.jwt_utils import create_access_token
from datetime import timedelta
from fastapi.security import HTTPBearer
from src.utils.jwt_utils import verify_token
from sqlmodel import select
from fastapi import Depends, HTTPException, status, Request
from src.models.user import User
from src.database import get_session
from typing import Annotated

# Create a simple HTTPBearer instance for token extraction
security = HTTPBearer()


auth_router = APIRouter()


@auth_router.post("/auth/register", response_model=UserRegisterResponse)
def register_user(
    user_register: UserRegisterRequest,
    session: Annotated[Session, Depends(get_session)]
):
    """
    Register a new user account
    """
    # Check if user already exists
    existing_user = AuthService.get_user_by_email(session, user_register.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Create user
    user_create = UserCreate(
        email=user_register.email,
        name=user_register.name,
        password=user_register.password
    )

    try:
        db_user = AuthService.register_user(session, user_create)

        # Return user response
        return UserRegisterResponse(
            id=db_user.id,
            email=db_user.email,
            name=db_user.name,
            created_at=db_user.created_at
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )


@auth_router.post("/auth/login", response_model=UserLoginResponse)
def login_user(
    user_login: UserLoginRequest,
    session: Annotated[Session, Depends(get_session)]
):
    """
    Authenticate user and return JWT token
    """
    user = AuthService.authenticate_user(
        session,
        user_login.email,
        user_login.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token = AuthService.create_access_token_for_user(user)

    return UserLoginResponse(access_token=access_token, token_type="bearer")


@auth_router.post("/auth/logout")
def logout_user():
    """
    Logout user (client-side token removal is sufficient since JWTs are stateless)
    """
    # For JWT tokens, the server doesn't need to store or invalidate the token
    # The client should remove the token from local storage/cookies
    return {"message": "Logged out successfully"}


async def get_current_user_from_token(request: Request, session: Annotated[Session, Depends(get_session)]) -> User:
    """Dependency to get current user from JWT token"""
    credentials = await security.__call__(request)

    if credentials:
        if not credentials.scheme == "Bearer":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid authentication scheme."
            )

        token_payload = verify_token(credentials.credentials)
        if not token_payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user_id = token_payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Fetch user from database
        try:
            statement = select(User).where(User.id == user_id)
            user = session.exec(statement).first()

            if not user:
                print(f"DEBUG: User with ID {user_id} not found in database")  # Debug print
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )

            print(f"DEBUG: Found user {user.email} with ID {user.id}")  # Debug print
            return user
        except Exception as e:
            print(f"DEBUG: Database query error: {str(e)}")  # Debug print
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Database error: {str(e)}"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authenticated"
        )


@auth_router.get("/auth/me")
def get_current_user_profile(
    current_user: User = Depends(get_current_user_from_token),
):
    """
    Get current authenticated user's information
    """
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name,
        "created_at": current_user.created_at
    }