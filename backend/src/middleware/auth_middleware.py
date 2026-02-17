from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from ..utils.jwt_utils import verify_token


class JWTBearer(HTTPBearer):
    """
    Custom JWT Bearer authentication scheme
    """
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(
            auto_error=auto_error,
            bearerFormat="JWT",
            description="Enter your JWT token to access protected endpoints"
        )

    async def __call__(self, request: Request) -> Optional[str]:
        """
        Extract and validate JWT token from request
        """
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)

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

            # Add user info to request state for use in endpoints
            request.state.user_id = token_payload.get("sub")
            request.state.user_email = token_payload.get("email")

            return credentials.credentials
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid authorization code."
            )


async def get_current_user_with_auth(request: Request):
    """
    Combined dependency that validates JWT token and returns user ID
    This ensures both validation and user ID extraction happen in one step
    """
    # First validate the token using our JWTBearer instance
    jwt_bearer = JWTBearer(auto_error=True)
    credentials: HTTPAuthorizationCredentials = await jwt_bearer.__call__(request)

    # Extract and return the user ID from the request state (set by the JWTBearer.__call__ method)
    user_id = getattr(request.state, 'user_id', None)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_id


def get_current_user_id(request: Request) -> str:
    """
    Get the current user ID from the request state
    """
    user_id = getattr(request.state, 'user_id', None)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_id


# Create a global instance of JWTBearer for OpenAPI documentation
jwt_security = JWTBearer(
    auto_error=True
)


# Define security scheme for OpenAPI
security_scheme = {
    "type": "http",
    "scheme": "bearer",
    "bearerFormat": "JWT",
    "description": "Enter your JWT token to access protected endpoints"
}


async def get_current_user(request: Request) -> dict:
    """
    Dependency that validates JWT token and returns user info dict.
    Used by chat API endpoints.
    """
    jwt_bearer = JWTBearer(auto_error=True)
    await jwt_bearer.__call__(request)

    user_id = getattr(request.state, 'user_id', None)
    user_email = getattr(request.state, 'user_email', None)

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {"user_id": user_id, "email": user_email}