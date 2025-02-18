from typing import Any, Dict

import pytest
from faker import Faker
from httpx import AsyncClient

fake = Faker()


@pytest.mark.asyncio
async def test_user_flow(client: AsyncClient, test_data: Dict[str, Any]) -> None:
    username = fake.user_name()
    password = fake.password(length=12)

    property_id = test_data["property_id"]

    # 1. Создаём таймзону
    tz_payload = {"timezone_name": fake.timezone(), "timezone": "12:00:00+00:00"}
    tz_response = await client.post("/v1/timezones/", json=tz_payload)
    assert tz_response.status_code == 201
    tz_data = tz_response.json()
    timezone_id = tz_data["id"]

    # 2. Создаём компанию
    company_payload = {
        "property_id": property_id,
        "name": fake.company(),
        "inn": fake.random_number(digits=10),
        "kpp": fake.random_number(digits=9),
        "ogrn": fake.random_number(digits=13),
        "bic": fake.random_number(digits=9),
    }
    comp_response = await client.post("/v1/companies/", json=company_payload)
    assert comp_response.status_code == 201
    comp_data = comp_response.json()
    company_id = comp_data["id"]

    # 3. Создаём группу для пользователя
    group_payload = {"company_id": company_id, "group_name": fake.word(), "comment": fake.sentence()}
    group_response = await client.post("/v1/groups/", json=group_payload)
    assert group_response.status_code == 201
    group_data = group_response.json()
    group_id = group_data["id"]

    # 4. Регистрируем
    user_payload = {
        "username": username,
        "password": password,
        "firstname": fake.first_name(),
        "lastname": fake.last_name(),
        "patronymic": fake.first_name(),
        "company_id": company_id,
        "group_id": group_id,
        "timezone_id": timezone_id,
    }
    user_signup_response = await client.post("/v1/auth/signup/user", json=user_payload)
    assert user_signup_response.status_code == 201
    user_signup_data = user_signup_response.json()
    user_data = user_signup_data.get("user")
    assert user_data["username"] == username

    # 5. Авторизация
    login_payload = {"username": user_payload["username"], "password": password}
    login_response = await client.post("/v1/auth/token", data=login_payload)
    assert login_response.status_code == 200
    token_data = login_response.json()
    access_token = token_data["access_token"]
    refresh_token = token_data["refresh_token"]

    # 6. Обновление access токена
    refresh_payload = {"refresh_token": refresh_token}
    refresh_response = await client.post("/v1/auth/token/refresh", json=refresh_payload)
    assert refresh_response.status_code == 200
    new_access_token = refresh_response.json()["access_token"]
    assert new_access_token != access_token

    # 7. Logout
    logout_payload = {"refresh_token": refresh_token}
    logout_response = await client.post("/v1/auth/logout", json=logout_payload)
    assert logout_response.status_code == 200
