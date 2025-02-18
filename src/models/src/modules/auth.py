from datetime import datetime

from sqlalchemy import TIMESTAMP, Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.models.src.models import Base


class Token(Base):
    __tablename__ = "tokens"

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", onupdate="CASCADE"), nullable=False)
    token: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    ua: Mapped[str] = mapped_column(String, nullable=True)
    ip: Mapped[str] = mapped_column(String, nullable=True)
    is_unlimited: Mapped[bool] = mapped_column(Boolean, default=False)

    expires_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=False), nullable=False)
