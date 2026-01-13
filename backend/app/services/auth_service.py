from datetime import datetime
from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_jwt_token,
    JWT_TYPE_REFRESH,
    JWT_OWNER_NAME,
    JWT_OWNER_FIELD,
)
from app.core.exceptions import InvalidTokenError
from app.services.user_service import get_user_by_id


def create_tokens_for_user(user: User) -> dict[str, str]:
    """Create access and refresh tokens for a user"""
    access_token = create_access_token(user.id, user.email, user.jwt_token_key)
    refresh_token = create_refresh_token(user.id, user.email, user.jwt_token_key)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


def refresh_access_token(db: Session, refresh_token: str) -> dict[str, str]:
    """Generate new access token from refresh token"""
    try:
        # Decode refresh token
        payload = decode_jwt_token(refresh_token, verify_expiration=True)

        # Verify it's a refresh token
        if payload.get("type") != JWT_TYPE_REFRESH:
            raise InvalidTokenError()

        # Verify owner
        if payload.get(JWT_OWNER_FIELD) != JWT_OWNER_NAME:
            raise InvalidTokenError()

        # Get user
        user_id = payload.get("user_id")
        user = get_user_by_id(db, user_id)

        if not user or not user.is_active:
            raise InvalidTokenError()

        # Verify token key hasn't been rotated
        if user.jwt_token_key != payload.get("token"):
            raise InvalidTokenError()

        # Update last login
        user.last_login = datetime.utcnow()
        db.commit()

        # Create new access token
        access_token = create_access_token(user.id, user.email, user.jwt_token_key)
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    except Exception:
        raise InvalidTokenError()
