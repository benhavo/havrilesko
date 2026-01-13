from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.sql import func
from secrets import token_urlsafe

from app.core.database import Base


def generate_jwt_token_key() -> str:
    """Generate random 12-character token key"""
    return token_urlsafe(9)[:12]  # URL-safe, ~12 chars


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # Authentication
    jwt_token_key = Column(String(12), default=generate_jwt_token_key, nullable=False)
    email_confirmed = Column(Boolean, default=False, nullable=False)

    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return f"<User {self.email}>"
