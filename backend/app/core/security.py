from datetime import datetime, timedelta
from typing import Any
from jose import jwt, JWTError
from passlib.context import CryptContext
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from app.core.config import get_settings

settings = get_settings()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT constants
JWT_TYPE_ACCESS = "access"
JWT_TYPE_REFRESH = "refresh"
JWT_OWNER_NAME = "havrilesko"
JWT_OWNER_FIELD = "owner"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


def get_private_key() -> rsa.RSAPrivateKey:
    """Load RSA private key from settings"""
    pem = settings.rsa_private_key.encode("utf-8")
    return serialization.load_pem_private_key(pem, password=None)


def get_public_key() -> rsa.RSAPublicKey:
    """Derive public key from private key"""
    return get_private_key().public_key()


def create_jwt_token(
    data: dict[str, Any],
    token_type: str,
    expires_delta: timedelta,
) -> str:
    """Create a JWT token with RSA256 signature"""
    utc_now = datetime.utcnow()

    payload = {
        "iat": utc_now,
        "exp": utc_now + expires_delta,
        "iss": f"https://{settings.jwt_issuer_domain}",
        JWT_OWNER_FIELD: JWT_OWNER_NAME,
        "type": token_type,
        **data,
    }

    # Encode with private key
    private_key = get_private_key()
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    return jwt.encode(payload, private_pem, algorithm=settings.jwt_algorithm)


def decode_jwt_token(token: str, verify_expiration: bool = True) -> dict[str, Any]:
    """Decode and verify JWT token"""
    public_key = get_public_key()
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    options = {
        "verify_exp": verify_expiration,
        "require": ["iat", "iss", "owner", "type"],
    }

    return jwt.decode(
        token, public_pem, algorithms=[settings.jwt_algorithm], options=options
    )


def create_access_token(user_id: int, email: str, token_key: str) -> str:
    """Create an access token for a user"""
    data = {
        "user_id": user_id,
        "email": email,
        "token": token_key,
    }
    expires_delta = timedelta(seconds=settings.jwt_ttl_access_seconds)
    return create_jwt_token(data, JWT_TYPE_ACCESS, expires_delta)


def create_refresh_token(user_id: int, email: str, token_key: str) -> str:
    """Create a refresh token for a user"""
    data = {
        "user_id": user_id,
        "email": email,
        "token": token_key,
    }
    expires_delta = timedelta(seconds=settings.jwt_ttl_refresh_seconds)
    return create_jwt_token(data, JWT_TYPE_REFRESH, expires_delta)
