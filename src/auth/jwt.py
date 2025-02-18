import uuid
from datetime import datetime, timedelta
from typing import Any

from fastapi import HTTPException, status
from jose import ExpiredSignatureError, JWTError, jwt
from jose.exceptions import JWTClaimsError

from src.config import get_app_settings

settings = get_app_settings()


class TokenHandler:
    @staticmethod
    def encode_token(data: dict[str, Any], secret_key: str, expires_in: float) -> tuple[str, datetime]:
        expire = datetime.utcnow() + timedelta(minutes=expires_in)
        payload = data.copy()
        payload.update({"exp": expire, "iat": datetime.utcnow(), "jti": str(uuid.uuid4())})
        token = jwt.encode(payload, secret_key, algorithm=settings.JWT_ALGORITHM)
        return token, expire

    @staticmethod
    def decode_token(token: str, secret_key: str) -> dict[str, Any]:
        try:
            payload = jwt.decode(token, secret_key, algorithms=[settings.JWT_ALGORITHM])
            return payload
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except (JWTClaimsError, JWTError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )

    @staticmethod
    def verify_token(token: str, secret_key: str) -> bool:
        try:
            payload = TokenHandler.decode_token(token, secret_key)
            return "user_data" in payload and payload["user_data"].get("id") is not None
        except HTTPException:
            return False

    @staticmethod
    def get_new_access_token(refresh_token: str) -> str:
        payload = TokenHandler.decode_token(refresh_token, settings.JWT_REFRESH_SECRET_KEY)
        user_data = payload.get("user_data")
        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        new_data = {"user_data": user_data}
        new_token, _ = TokenHandler.encode_token(
            new_data, settings.JWT_ACCESS_SECRET_KEY, float(settings.JWT_ACCESS_TOKEN_EXPIRES_IN)
        )
        return new_token
