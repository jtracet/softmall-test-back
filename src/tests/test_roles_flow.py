import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_roles_flow(client: AsyncClient) -> None:
    # 1. Создаём роль
    role_payload = {"code": "admin", "name": "Administrator"}
    role_response = await client.post("/v1/roles/", json=role_payload)
    assert role_response.status_code == 201
    role_data = role_response.json()
    role_id = role_data["id"]

    # 2. Создаём функцию
    function_payload = {"code": "edit", "version": 1}
    function_response = await client.post("/v1/roles/functions", json=function_payload)
    assert function_response.status_code == 201
    function_data = function_response.json()
    function_id = function_data["id"]

    # 3. Назначаем функцию роли
    assign_payload = {"role_id": role_id, "function_ids": [function_id]}
    assign_response = await client.post("/v1/roles/assign-functions", json=assign_payload)
    assert assign_response.status_code == 200
    assign_detail = assign_response.json()
    assert assign_detail["detail"] == "Functions assigned"
