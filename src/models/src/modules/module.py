import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import BigInteger, Date, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.src import Base

if TYPE_CHECKING:
    from src.models.src.modules.company import Company


class Module(Base):
    __tablename__ = "modules"
    __table_args__ = (
        Index("idx_modules_code", "code"),
        {"comment": "Таблица дополнительных модулей"},
    )

    code: Mapped[str] = mapped_column(String(30), nullable=False)
    name: Mapped[str] = mapped_column(String(60), nullable=False)

    module_company_links: Mapped[List["ModuleCompanyLink"]] = relationship(
        "ModuleCompanyLink", back_populates="module"
    )


class ModuleCompanyLink(Base):
    __tablename__ = "module_company_links"
    __table_args__ = (
        Index("idx_module_company_links_company_id", "company_id"),
        Index("idx_module_company_links_module_id", "module_id"),
        Index("idx_module_company_links_active_from", "active_from"),
        Index("idx_module_company_links_active_to", "active_to"),
        Index("idx_module_company_links_company_id_active_from_active_to", "company_id", "active_from", "active_to"),
        {"comment": "Таблица связей модулей и компаний"},
    )

    module_id: Mapped[int] = mapped_column(Integer, ForeignKey("modules.id"), nullable=False)
    company_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("companies.id"), nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    active_from: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    active_to: Mapped[datetime.date | None] = mapped_column(Date, nullable=True)

    module: Mapped[Module] = relationship("Module", back_populates="module_company_links")
    company: Mapped["Company"] = relationship("Company", back_populates="module_company_links")
