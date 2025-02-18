import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import Index, Integer, String, Text, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.src import Base

if TYPE_CHECKING:
    from src.models.src.modules.company import Company, CompanyProperty
    from src.models.src.modules.user import User, UserProperty, UserReportLink, UserSending


class TimezoneDict(Base):
    __tablename__ = "timezone_dict"
    __table_args__ = {"comment": "Таблица с справчоник таймзон"}

    timezone_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    timezone: Mapped[datetime.time | None] = mapped_column(Time(timezone=True), nullable=True)

    users: Mapped[List["User"]] = relationship("User", back_populates="timezone")


class PropertyCodeDict(Base):
    __tablename__ = "property_code_dict"
    __table_args__ = (
        Index("idx_property_code_dict_code", "code"),
        Index("idx_property_code_dict_group_code_code", "group_code", "code"),
        {
            "comment": (
                "Таблица справочник кодов для свойств пользователя\n"
                "PROFILE_IMAGE - путь до картинки с профилем пользователя\n"
                "USER_MOBILE - телефон пользователя\n"
                "USER_NUMVER - индиыидуальный номер пользователя"
            )
        },
    )

    group_code: Mapped[str] = mapped_column(String(30), nullable=False)
    code: Mapped[str] = mapped_column(String(30), nullable=False)
    name: Mapped[str | None] = mapped_column(String(100), nullable=True)

    companies: Mapped[List["Company"]] = relationship("Company", back_populates="property_code")
    user_properties: Mapped[List["UserProperty"]] = relationship("UserProperty", back_populates="property_code")
    company_properties: Mapped[List["CompanyProperty"]] = relationship(
        "CompanyProperty", back_populates="property_code"
    )


class StatusDict(Base):
    __tablename__ = "status_dict"
    __table_args__ = (Index("idx_status_dict_code", "code"),)

    code: Mapped[str] = mapped_column(String(16), nullable=False)
    name: Mapped[str] = mapped_column(String(60), nullable=False)

    user_sendings: Mapped[List["UserSending"]] = relationship("UserSending", back_populates="status")


class ShablonDict(Base):
    __tablename__ = "shablon_dict"
    __table_args__ = (
        Index("idx_shablon_dict_code", "code"),
        {"comment": "Таблици справочник шаблонов"},
    )

    code: Mapped[str] = mapped_column(String(30), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    value: Mapped[str | None] = mapped_column(Text, nullable=True)


class Report(Base):
    __tablename__ = "reports"
    __table_args__ = (
        Index("idx_reports_code", "code"),
        Index("idx_reports_code_version", "code", "version"),
        {"comment": "Таблица справочник отчетов"},
    )

    code: Mapped[str] = mapped_column(String(30), nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False)

    user_report_links: Mapped[List["UserReportLink"]] = relationship("UserReportLink", back_populates="report")
