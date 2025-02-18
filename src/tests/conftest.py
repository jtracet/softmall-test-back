import asyncio
from typing import Any, AsyncGenerator, Dict

import httpx
import pytest
import pytest_asyncio
from dotenv import load_dotenv
from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from src.database import Session
from src.main import app
from src.models.src import PropertyCodeDict, SettingsDict, StatusDict


@pytest.fixture(autouse=True)
def load_env() -> None:
    load_dotenv(".env")


@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
def event_loop() -> Any:  # type: ignore
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[Session, None]:

    async with Session() as session:
        try:
            yield session
            await session.commit()
        except SQLAlchemyError as exc:
            await session.rollback()
            raise exc
        finally:
            await session.close()


@pytest_asyncio.fixture(scope="function")
async def test_data(db_session: Session) -> AsyncGenerator[Dict[str, Any], None]:
    property_record = PropertyCodeDict(group_code="company", code="default_company", name="Default Company Property")
    status_record = StatusDict(code="active", name="Active")
    settings_record = SettingsDict(code="site_title", name="Site Title")
    db_session.add_all([property_record, status_record, settings_record])
    await db_session.flush()
    await db_session.refresh(property_record)
    await db_session.refresh(status_record)
    await db_session.refresh(settings_record)
    await db_session.commit()

    test_ids = {"property_id": property_record.id, "status_id": status_record.id, "settings_id": settings_record.id}
    yield test_ids

    try:
        await db_session.execute(
            text("DELETE FROM settings WHERE setting_code_id = :code_id"), {"code_id": settings_record.id}
        )
        await db_session.execute(
            text(
                "DELETE FROM users WHERE group_id IN (SELECT id FROM user_groups WHERE company_id IN (SELECT id FROM companies WHERE property_id = :prop_id))"
            ),
            {"prop_id": property_record.id},
        )
        await db_session.execute(
            text(
                "DELETE FROM user_groups WHERE company_id IN (SELECT id FROM companies WHERE property_id = :prop_id)"
            ),
            {"prop_id": property_record.id},
        )
        await db_session.execute(
            text("DELETE FROM companies WHERE property_id = :prop_id"), {"prop_id": property_record.id}
        )
        await db_session.delete(property_record)
        await db_session.delete(status_record)
        await db_session.delete(settings_record)
        await db_session.commit()
    except SQLAlchemyError as exc:
        await db_session.rollback()
        raise exc
