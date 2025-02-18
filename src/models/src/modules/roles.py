from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, Index, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.src import Base

if TYPE_CHECKING:
    from src.models.src.modules.user import UserRole


class RolesDict(Base):
    __tablename__ = "roles_dict"
    __table_args__ = {"comment": "Таблица справочник ролей пользователя"}

    code: Mapped[str] = mapped_column(String(30), nullable=False)
    name: Mapped[str] = mapped_column(String(60), nullable=False)

    user_roles: Mapped[List["UserRole"]] = relationship("UserRole", back_populates="role")
    role_functions: Mapped[List["RoleFunction"]] = relationship("RoleFunction", back_populates="role")


class RoleFunction(Base):
    __tablename__ = "role_functions"
    __table_args__ = (
        Index("idx_role_functions_role_id", "role_id"),
        Index("idx_role_functions_function_code_id", "function_code_id"),
        {"comment": "Таблица с ролевыми функциями"},
    )

    role_id: Mapped[int] = mapped_column(SmallInteger, ForeignKey("roles_dict.id"), nullable=False)
    function_code_id: Mapped[int] = mapped_column(SmallInteger, ForeignKey("functions_dict.id"), nullable=False)

    role: Mapped[RolesDict] = relationship("RolesDict", back_populates="role_functions")
    function: Mapped["FunctionDict"] = relationship("FunctionDict", back_populates="role_functions")


class FunctionDict(Base):
    __tablename__ = "functions_dict"
    __table_args__ = {"comment": "Таблица справочник ролевых функций"}

    code: Mapped[str] = mapped_column(String(30), nullable=False)
    version: Mapped[int] = mapped_column(SmallInteger, nullable=False)

    role_functions: Mapped[List[RoleFunction]] = relationship("RoleFunction", back_populates="function")
