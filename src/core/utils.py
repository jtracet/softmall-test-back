import base64
import re
import uuid

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def uuid_to_base32(uuid_code: uuid.UUID) -> str:
    uuid_bytes = uuid_code.bytes
    return base64.b32encode(uuid_bytes).decode().rstrip("=")


def checking_received_username(username: str) -> str:
    if username.startswith("+") and username[1:].isdigit():
        return "phone"
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    if re.fullmatch(email_pattern, username):
        return "email"
    return "username"
