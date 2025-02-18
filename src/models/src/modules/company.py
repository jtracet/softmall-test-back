import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import BigInteger, Date, ForeignKey, Index, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.src import Base
from src.models.src.modules.dicts import PropertyCodeDict
from src.models.src.modules.module import ModuleCompanyLink

if TYPE_CHECKING:
    from src.models.src.modules.user import User, UserGroup


class Company(Base):
    __tablename__ = "companies"
    __table_args__ = (
        Index("idx_companies_inn", "inn"),
        Index("idx_companies_kpp", "kpp"),
        Index("idx_companies_ogrn", "ogrn"),
        Index("idx_companies_bic", "bic"),
        Index("idx_companies_property_id", "property_id"),
        {"comment": "Таблица с компаниями"},
    )

    property_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("property_code_dict.id"), nullable=False)
    name: Mapped[str] = mapped_column("name", String(255), nullable=False)
    created_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    inn: Mapped[str] = mapped_column(String(16), nullable=False)
    kpp: Mapped[str] = mapped_column(String(9), nullable=False)
    ogrn: Mapped[str | None] = mapped_column(String(13), nullable=True)
    bic: Mapped[str | None] = mapped_column(String(9), nullable=True)

    property_code: Mapped[PropertyCodeDict] = relationship("PropertyCodeDict", back_populates="companies")
    users: Mapped[List["User"]] = relationship("User", back_populates="company")
    user_groups: Mapped[List["UserGroup"]] = relationship("UserGroup", back_populates="company")
    licenses: Mapped[List["License"]] = relationship("License", back_populates="company")
    module_company_links: Mapped[List[ModuleCompanyLink]] = relationship("ModuleCompanyLink", back_populates="company")
    company_properties: Mapped[List["CompanyProperty"]] = relationship("CompanyProperty", back_populates="company")
    departments: Mapped[List["Department"]] = relationship("Department", back_populates="company")


class CompanyProperty(Base):
    __tablename__ = "company_properties"
    __table_args__ = (
        Index("idx_company_properties_company_id", "company_id"),
        Index("idx_company_properties_company_id_property_code_id", "company_id", "property_code_id"),
        {"comment": "Таблица свойств компаний"},
    )

    company_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("companies.id"), nullable=False)
    property_code_id: Mapped[int] = mapped_column(SmallInteger, ForeignKey("property_code_dict.id"), nullable=False)
    value: Mapped[str | None] = mapped_column(String(255), nullable=True)

    company: Mapped[Company] = relationship("Company", back_populates="company_properties")
    property_code: Mapped[PropertyCodeDict] = relationship("PropertyCodeDict", back_populates="company_properties")


class Department(Base):
    __tablename__ = "departments"
    __table_args__ = (
        Index("idx_departments_code", "code"),
        Index("idx_departments_company_id", "company_id"),
        {"comment": "Таблица с подраздлений"},
    )

    company_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("companies.id"), nullable=False)
    code: Mapped[int] = mapped_column(BigInteger, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)

    company: Mapped[Company] = relationship("Company", back_populates="departments")


class License(Base):
    __tablename__ = "license"
    __table_args__ = (
        Index("idx_license_company_id", "company_id"),
        Index("idx_license_company_id_active_from", "company_id", "active_from"),
        Index("idx_license_active_from_active_to", "active_from", "active_to"),
        Index("idx_license_company_id_active_from_active_to", "company_id", "active_from", "active_to"),
        {"comment": "Таблица с лицензиями"},
    )

    company_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("companies.id"), nullable=False)
    lisense_key: Mapped[str] = mapped_column(String(1000), nullable=False)
    active_from: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    active_to: Mapped[datetime.date] = mapped_column(Date, nullable=False)

    company: Mapped[Company] = relationship("Company", back_populates="licenses")
