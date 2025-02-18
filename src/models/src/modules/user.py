import datetime
from typing import List

from sqlalchemy import BigInteger, Boolean, Date, ForeignKey, Index, Integer, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.src import Base
from src.models.src.modules.company import Company
from src.models.src.modules.dicts import PropertyCodeDict, Report, StatusDict, TimezoneDict
from src.models.src.modules.roles import RolesDict


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        Index("idx_users_group_id", "group_id"),
        Index("idx_users_timezone_id", "timezone_id"),
        Index("idx_users_company_id", "company_id"),
        Index("idx_users_username", "username"),
        Index("idx_users_company_id_group_id", "company_id", "group_id"),
        Index("idx_users_username_user_lock", "username", "user_lock"),
        Index("idx_users_id_company_id", "id", "company_id"),
        Index("idx_users_id_group_id", "id", "group_id"),
        Index("idx_users_id_property_id", "id"),
        {"comment": "Таблица пользователей"},
    )

    company_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("companies.id"), nullable=False)
    group_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("user_groups.id"), nullable=False)
    timezone_id: Mapped[int] = mapped_column(SmallInteger, ForeignKey("timezone_dict.id"), nullable=False)
    username: Mapped[str] = mapped_column(String(60), nullable=False, index=True)
    firstname: Mapped[str] = mapped_column(String(60), nullable=False)
    lastname: Mapped[str] = mapped_column(String(60), nullable=False)
    patronymic: Mapped[str | None] = mapped_column(String(60), nullable=True)
    created_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    user_lock: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    password: Mapped[str] = mapped_column("password", String(255), nullable=False)
    comment: Mapped[str | None] = mapped_column("comment", String(1000), nullable=True)

    company: Mapped[Company] = relationship("Company", back_populates="users")
    group: Mapped["UserGroup"] = relationship("UserGroup", back_populates="users")
    timezone: Mapped[TimezoneDict] = relationship("TimezoneDict", back_populates="users")
    roles: Mapped[List["UserRole"]] = relationship("UserRole", back_populates="user")
    properties: Mapped[List["UserProperty"]] = relationship("UserProperty", back_populates="user")
    sendings: Mapped[List["UserSending"]] = relationship("UserSending", back_populates="user")
    report_links: Mapped[List["UserReportLink"]] = relationship("UserReportLink", back_populates="user")


class UserGroup(Base):
    __tablename__ = "user_groups"
    __table_args__ = (
        Index("idx_user_groups_company_id", "company_id"),
        {"comment": "Таблица групп пользователей"},
    )

    company_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("companies.id"), nullable=False)
    group_name: Mapped[str] = mapped_column(String(255), nullable=False)
    comment: Mapped[str | None] = mapped_column("comment", String(1000), nullable=True)

    company: Mapped[Company] = relationship("Company", back_populates="user_groups")
    users: Mapped[List[User]] = relationship("User", back_populates="group")


class UserProperty(Base):
    __tablename__ = "user_properties"
    __table_args__ = (
        Index("idx_user_properties_property_id", "user_id"),
        Index("idx_user_properties_property_id_property_code_id", "user_id", "property_code_id"),
        {"comment": "Таблица свойств пользователей"},
    )

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=False)
    property_code_id: Mapped[int] = mapped_column(SmallInteger, ForeignKey("property_code_dict.id"), nullable=False)
    value: Mapped[str | None] = mapped_column(String(255), nullable=True)

    user: Mapped[User] = relationship("User", back_populates="properties")
    property_code: Mapped[PropertyCodeDict] = relationship("PropertyCodeDict", back_populates="user_properties")


class UserRole(Base):
    __tablename__ = "user_roles"
    __table_args__ = (
        Index("idx_user_roles_user_id", "user_id"),
        Index("idx_user_roles_role_id", "role_id"),
        Index("idx_user_roles_user_id_role_id_active_to", "user_id", "role_id", "active_to"),
        Index("idx_user_roles_active_from", "active_from"),
        Index("idx_user_roles_active_to", "active_to"),
        {"comment": "Таблица ролей пользователей"},
    )

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=False)
    role_id: Mapped[int] = mapped_column(SmallInteger, ForeignKey("roles_dict.id"), nullable=False)
    active_from: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    active_to: Mapped[datetime.date | None] = mapped_column(Date, nullable=True)

    user: Mapped[User] = relationship("User", back_populates="roles")
    role: Mapped[RolesDict] = relationship("RolesDict", back_populates="user_roles")


class UserSending(Base):
    __tablename__ = "user_sendings"
    __table_args__ = (
        Index("idx_user_sendings_user_id", "user_id"),
        Index("idx_user_sendings_status_id", "status_id"),
        Index("idx_user_sendings_user_id_status_id_created_date", "user_id", "status_id", "created_date"),
        Index("idx_user_sendings_created_date", "created_date"),
        {"comment": "Таблица рассылки сообщений по пользователям"},
    )

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=False, unique=True)
    status_id: Mapped[int] = mapped_column(Integer, ForeignKey("status_dict.id"), nullable=False)
    created_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    message: Mapped[str] = mapped_column(String(4000), nullable=False)

    user: Mapped[User] = relationship("User", back_populates="sendings")
    status: Mapped[StatusDict] = relationship("StatusDict", back_populates="user_sendings")


class UserReportLink(Base):
    __tablename__ = "user_report_links"
    __table_args__ = (
        Index("idx_user_report_links_user_id", "user_id"),
        Index("idx_user_report_links_report_id", "report_id"),
        Index("idx_user_report_links_created_date", "created_date"),
        Index("idx_user_report_links_acive_from", "acive_from"),
        Index("idx_user_report_links_active_to", "active_to"),
        Index("idx_user_report_links_acive_from_active_to", "acive_from", "active_to"),
        Index("idx_user_report_links_user_id_active_to", "user_id", "active_to"),
        Index("idx_user_report_links_user_id_acive_from_active_to", "user_id", "acive_from", "active_to"),
        Index("idx_user_report_links_id", "id"),
        {"comment": "Таблица связей отчетов и пользователей"},
    )

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=False)
    report_id: Mapped[int] = mapped_column(Integer, ForeignKey("reports.id"), nullable=False)
    created_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    acive_from: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    active_to: Mapped[datetime.date | None] = mapped_column(Date, nullable=True)

    user: Mapped[User] = relationship("User", back_populates="report_links")
    report: Mapped[Report] = relationship("Report", back_populates="user_report_links")
