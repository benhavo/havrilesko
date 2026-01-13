from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session
from jose import JWTError

from app.core.database import get_db
from app.core.security import (
    decode_jwt_token,
    JWT_TYPE_ACCESS,
    JWT_OWNER_NAME,
    JWT_OWNER_FIELD,
)
from app.core.exceptions import AuthenticationError, InvalidTokenError, InactiveUserError
from app.models.user import User
from app.services.user_service import get_user_by_id


def get_token_from_header(authorization: str = Header(None)) -> str:
    """Extract JWT token from Authorization header"""
    if not authorization:
        raise AuthenticationError()

    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() not in ["bearer", "jwt"]:
        raise AuthenticationError()

    return parts[1]


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(get_token_from_header)
) -> User:
    """Get current authenticated user from JWT token"""
    try:
        # Decode token
        payload = decode_jwt_token(token, verify_expiration=True)

        # Verify token type
        if payload.get("type") != JWT_TYPE_ACCESS:
            raise InvalidTokenError()

        # Verify owner
        if payload.get(JWT_OWNER_FIELD) != JWT_OWNER_NAME:
            raise InvalidTokenError()

        # Get user
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise InvalidTokenError()

        user = get_user_by_id(db, user_id)
        if not user:
            raise InvalidTokenError()

        # Verify token key
        if user.jwt_token_key != payload.get("token"):
            raise InvalidTokenError()

        # Check if user is active
        if not user.is_active:
            raise InactiveUserError()

        return user

    except JWTError:
        raise InvalidTokenError()


def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    """Dependency for superuser-only routes"""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user
