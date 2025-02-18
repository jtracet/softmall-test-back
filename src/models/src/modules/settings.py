import datetime
from typing import List

from sqlalchemy import Date, ForeignKey, Index, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.src import Base


class Settings(Base):
    __tablename__ = "settings"
    __table_args__ = (
        Index("idx_settings_setting_code_id", "setting_code_id"),
        Index("idx_settings_active_from", "active_from"),
        Index("idx_settings_active_to", "active_to"),
        Index("idx_settings_active_from_active_to", "active_from", "active_to"),
        Index("idx_settings_property_code_id_active_from_active_to", "setting_code_id", "active_from", "active_to"),
        Index("idx_settings_setting_code_id_active_to", "setting_code_id", "active_to"),
        {"comment": "Таблица общих свойст"},
    )

    setting_code_id: Mapped[int] = mapped_column(SmallInteger, ForeignKey("settings_dict.id"), nullable=False)
    value: Mapped[str] = mapped_column(String(255), nullable=False)
    active_from: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    active_to: Mapped[datetime.date | None] = mapped_column(Date, nullable=True)

    settings_dict: Mapped["SettingsDict"] = relationship("SettingsDict", back_populates="settings")


class SettingsDict(Base):
    __tablename__ = "settings_dict"
    __table_args__ = (
        Index("idx_settings_dict_code", "code"),
        {"comment": "Таблица справочник кодов системы"},
    )

    code: Mapped[str] = mapped_column(String(30), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    settings: Mapped[List[Settings]] = relationship("Settings", back_populates="settings_dict")
