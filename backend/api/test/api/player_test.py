import pytest
from fastapi import status
from httpx import AsyncClient

pytestmark = pytest.mark.anyio


@pytest.mark.parametrize(
    "payload, status_code",
    (
        (
            {"name": "Puppey", "steamid": 76561198047544485, "opendota_link": "https://www.opendota.com/players/87278757"},
            status.HTTP_201_CREATED,
        ),
    ),
)
async def test_add_stuff(client: AsyncClient, payload: dict, status_code: int):
    response = await client.post("/player/", params=payload)
    assert response.status_code == status_code
    assert payload["name"] == response.json()["name"]
