from typing import Any, Dict

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_settings_flow(client: AsyncClient, test_data: Dict[str, Any]) -> None:
    # 1. Создаём настройку
    setting_code_id = test_data["settings_id"]
    setting_payload = {
        "setting_code_id": setting_code_id,
        "value": "Initial Value",
        "active_from": "2023-01-01",
        "active_to": "2023-12-31",
    }
    setting_response = await client.post("/v1/settings/", json=setting_payload)
    assert setting_response.status_code == 201
    setting_data = setting_response.json()
    setting_id = setting_data["id"]

    # 2. Обновляем настройку
    update_payload = {
        "setting_code_id": setting_code_id,
        "value": "Updated Value",
        "active_from": "2023-01-01",
        "active_to": "2023-12-31",
    }

    update_response = await client.put(f"/v1/settings/{setting_id}", json=update_payload)
    assert update_response.status_code == 200
    updated_setting = update_response.json()
    assert updated_setting["value"] == "Updated Value"
