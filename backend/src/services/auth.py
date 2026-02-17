from sqlmodel import Session, select
from typing import Optional
from datetime import timedelta
from ..models.user import User, UserCreate
from ..utils.jwt_utils import verify_password, get_password_hash, create_access_token


class AuthService:
    """
    Service class for handling authentication-related operations
    """

    @staticmethod
    def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
        """
        Authenticate a user with email and password
        """
        # Find user by email
        statement = select(User).where(User.email == email)
        user = session.exec(statement).first()

        if not user or not verify_password(password, user.password_hash):
            return None

        return user

    @staticmethod
    def create_access_token_for_user(user: User) -> str:
        """
        Create an access token for the given user
        """
        data = {"sub": user.id, "email": user.email}
        expires = timedelta(minutes=30)  # Use default from settings
        return create_access_token(data=data, expires_delta=expires)

    @staticmethod
    def register_user(session: Session, user_create: UserCreate) -> User:
        """
        Register a new user with the given details
        """
        # Hash the password
        hashed_password = get_password_hash(user_create.password)

        # Create the user instance
        db_user = User(
            email=user_create.email,
            name=user_create.name,
            password_hash=hashed_password
        )

        # Add to session and commit
        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        return db_user

    @staticmethod
    def get_user_by_email(session: Session, email: str) -> Optional[User]:
        """
        Retrieve a user by email
        """
        statement = select(User).where(User.email == email)
        return session.exec(statement).first()