from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import JWTError
from typing import Optional
from src.config import settings


security = HTTPBearer()


def decode_token(token: str) -> dict:
    """
    Decode a JWT token and return the payload.

    Args:
        token: JWT token to decode

    Returns:
        Decoded token payload

    Raises:
        JWTError: If the token is invalid or expired
    """
    try:
        # In a real application, you'd use a proper secret and algorithm
        # For this example, we'll use the secret from settings
        payload = jwt.decode(
            token,
            settings.BETTER_AUTH_SECRET,
            algorithms=["HS256"]
        )
        return payload

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Get the current user ID from the JWT token in the Authorization header.

    Args:
        credentials: HTTP authorization credentials from the header

    Returns:
        User ID extracted from the token
    """
    token = credentials.credentials

    payload = decode_token(token)

    # Try to get user ID from various possible fields in the token
    user_id = payload.get("user_id") or payload.get("userId") or payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return str(user_id)


def verify_user_access(user_id: str, current_user_id: str = Depends(get_current_user_id)) -> bool:
    """
    Verify that the current authenticated user has access to the specified user ID.

    Args:
        user_id: The user ID being accessed
        current_user_id: The authenticated user's ID (from JWT)

    Returns:
        True if the current user has access to the specified user ID

    Raises:
        HTTPException: If the user doesn't have access
    """
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Insufficient permissions"
        )

    return True


# Additional helper function for creating tokens (for testing purposes)
def create_access_token(data: dict, expires_delta: Optional[int] = None):
    """
    Create a JWT access token.

    Args:
        data: Data to encode in the token
        expires_delta: Token expiration time in seconds

    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, settings.BETTER_AUTH_SECRET, algorithm="HS256")
    return encoded_jwt