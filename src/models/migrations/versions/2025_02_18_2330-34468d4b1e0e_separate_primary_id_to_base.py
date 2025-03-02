"""separate primary id to base

Revision ID: 34468d4b1e0e
Revises: fc82411fd269
Create Date: 2025-02-18 23:30:54.646122

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "34468d4b1e0e"
down_revision: Union[str, None] = "fc82411fd269"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "companies",
        "id",
        existing_type=sa.BIGINT(),
        type_=sa.Integer(),
        existing_nullable=False,
        autoincrement=True,
        existing_server_default=sa.text("nextval('companies_id_seq'::regclass)"),
    )
    op.alter_column(
        "company_properties",
        "id",
        existing_type=sa.BIGINT(),
        type_=sa.Integer(),
        existing_nullable=False,
        autoincrement=True,
    )
    op.alter_column(
        "departments", "id", existing_type=sa.BIGINT(), type_=sa.Integer(), existing_nullable=False, autoincrement=True
    )
    op.alter_column(
        "functions_dict",
        "id",
        existing_type=sa.SMALLINT(),
        type_=sa.Integer(),
        existing_nullable=False,
        autoincrement=True,
        existing_server_default=sa.text("nextval('functions_dict_id_seq'::regclass)"),
    )
    op.alter_column(
        "license", "id", existing_type=sa.BIGINT(), type_=sa.Integer(), existing_nullable=False, autoincrement=True
    )
    op.alter_column(
        "module_company_links",
        "id",
        existing_type=sa.BIGINT(),
        type_=sa.Integer(),
        existing_nullable=False,
        autoincrement=True,
    )
    op.alter_column(
        "property_code_dict",
        "id",
        existing_type=sa.SMALLINT(),
        type_=sa.Integer(),
        existing_nullable=False,
        autoincrement=True,
        existing_server_default=sa.text("nextval('property_code_dict_id_seq'::regclass)"),
    )
    op.alter_column(
        "role_functions",
        "id",
        existing_type=sa.SMALLINT(),
        type_=sa.Integer(),
        existing_nullable=False,
        autoincrement=True,
        existing_server_default=sa.text("nextval('role_functions_id_seq'::regclass)"),
    )
    op.alter_column(
        "roles_dict",
        "id",
        existing_type=sa.SMALLINT(),
        type_=sa.Integer(),
        existing_nullable=False,
        autoincrement=True,
        existing_server_default=sa.text("nextval('roles_dict_id_seq'::regclass)"),
    )
    op.alter_column(
        "settings",
        "id",
        existing_type=sa.SMALLINT(),
        type_=sa.Integer(),
        existing_nullable=False,
        autoincrement=True,
        existing_server_default=sa.text("nextval('settings_id_seq'::regclass)"),
    )
    op.alter_column(
        "settings_dict",
        "id",
        existing_type=sa.SMALLINT(),
        type_=sa.Integer(),
        existing_nullable=False,
        autoincrement=True,
        existing_server_default=sa.text("nextval('settings_dict_id_seq'::regclass)"),
    )
    op.alter_column(
        "timezone_dict",
        "id",
        existing_type=sa.SMALLINT(),
        type_=sa.Integer(),
        existing_nullable=False,
        autoincrement=True,
        existing_server_default=sa.text("nextval('timezone_dict_id_seq'::regclass)"),
    )
    op.alter_column(
        "user_groups",
        "id",
        existing_type=sa.BIGINT(),
        type_=sa.Integer(),
        existing_nullable=False,
        autoincrement=True,
        existing_server_default=sa.text("nextval('user_groups_id_seq'::regclass)"),
    )
    op.alter_column(
        "user_properties",
        "id",
        existing_type=sa.BIGINT(),
        type_=sa.Integer(),
        existing_nullable=False,
        autoincrement=True,
    )
    op.alter_column(
        "user_report_links",
        "id",
        existing_type=sa.BIGINT(),
        type_=sa.Integer(),
        existing_nullable=False,
        autoincrement=True,
    )
    op.alter_column(
        "user_sendings",
        "id",
        existing_type=sa.BIGINT(),
        type_=sa.Integer(),
        existing_nullable=False,
        autoincrement=True,
    )
    op.alter_column(
        "users",
        "id",
        existing_type=sa.BIGINT(),
        type_=sa.Integer(),
        existing_nullable=False,
        autoincrement=True,
        existing_server_default=sa.text("nextval('users_id_seq'::regclass)"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "users",
        "id",
        existing_type=sa.Integer(),
        type_=sa.BIGINT(),
        existing_nullable=False,
        autoincrement=True,
        existing_server_default=sa.text("nextval('users_id_seq'::regclass)"),
    )
    op.alter_column(
        "user_sendings",
        "id",
        existing_type=sa.Integer(),
        type_=sa.BIGINT(),
        existing_nullable=False,
        autoincrement=True,
    )
    op.alter_column(
        "user_report_links",
        "id",
        existing_type=sa.Integer(),
        type_=sa.BIGINT(),
        existing_nullable=False,
        autoincrement=True,
    )
    op.alter_column(
        "user_properties",
        "id",
        existing_type=sa.Integer(),
        type_=sa.BIGINT(),
        existing_nullable=False,
        autoincrement=True,
    )
    op.alter_column(
        "user_groups",
        "id",
        existing_type=sa.Integer(),
        type_=sa.BIGINT(),
        existing_nullable=False,
        autoincrement=True,
        existing_server_default=sa.text("nextval('user_groups_id_seq'::regclass)"),
    )
    op.alter_column(
        "timezone_dict",
        "id",
        existing_type=sa.Integer(),
        type_=sa.SMALLINT(),
        existing_nullable=False,
        autoincrement=True,
        existing_server_default=sa.text("nextval('timezone_dict_id_seq'::regclass)"),
    )
    op.alter_column(
        "settings_dict",
        "id",
        existing_type=sa.Integer(),
        type_=sa.SMALLINT(),
        existing_nullable=False,
        autoincrement=True,
        existing_server_default=sa.text("nextval('settings_dict_id_seq'::regclass)"),
    )
    op.alter_column(
        "settings",
        "id",
        existing_type=sa.Integer(),
        type_=sa.SMALLINT(),
        existing_nullable=False,
        autoincrement=True,
        existing_server_default=sa.text("nextval('settings_id_seq'::regclass)"),
    )
    op.alter_column(
        "roles_dict",
        "id",
        existing_type=sa.Integer(),
        type_=sa.SMALLINT(),
        existing_nullable=False,
        autoincrement=True,
        existing_server_default=sa.text("nextval('roles_dict_id_seq'::regclass)"),
    )
    op.alter_column(
        "role_functions",
        "id",
        existing_type=sa.Integer(),
        type_=sa.SMALLINT(),
        existing_nullable=False,
        autoincrement=True,
        existing_server_default=sa.text("nextval('role_functions_id_seq'::regclass)"),
    )
    op.alter_column(
        "property_code_dict",
        "id",
        existing_type=sa.Integer(),
        type_=sa.SMALLINT(),
        existing_nullable=False,
        autoincrement=True,
        existing_server_default=sa.text("nextval('property_code_dict_id_seq'::regclass)"),
    )
    op.alter_column(
        "module_company_links",
        "id",
        existing_type=sa.Integer(),
        type_=sa.BIGINT(),
        existing_nullable=False,
        autoincrement=True,
    )
    op.alter_column(
        "license", "id", existing_type=sa.Integer(), type_=sa.BIGINT(), existing_nullable=False, autoincrement=True
    )
    op.alter_column(
        "functions_dict",
        "id",
        existing_type=sa.Integer(),
        type_=sa.SMALLINT(),
        existing_nullable=False,
        autoincrement=True,
        existing_server_default=sa.text("nextval('functions_dict_id_seq'::regclass)"),
    )
    op.alter_column(
        "departments", "id", existing_type=sa.Integer(), type_=sa.BIGINT(), existing_nullable=False, autoincrement=True
    )
    op.alter_column(
        "company_properties",
        "id",
        existing_type=sa.Integer(),
        type_=sa.BIGINT(),
        existing_nullable=False,
        autoincrement=True,
    )
    op.alter_column(
        "companies",
        "id",
        existing_type=sa.Integer(),
        type_=sa.BIGINT(),
        existing_nullable=False,
        autoincrement=True,
        existing_server_default=sa.text("nextval('companies_id_seq'::regclass)"),
    )
    # ### end Alembic commands ###
