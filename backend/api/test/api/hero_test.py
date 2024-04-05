from typing import Optional

import pytest
from fastapi import status
from httpx import AsyncClient

pytestmark = pytest.mark.anyio


@pytest.mark.parametrize(
    "payload, status_code",
    (
        (
            {
                "opendota_name": "nevermore"
            },
            status.HTTP_201_CREATED,
        ),
        (
            {
                "opendota_name": "nevermore"
            },
            status.HTTP_400_BAD_REQUEST,
        ),
    ),
)
async def test_add_hero(client: AsyncClient, payload: dict, status_code: int):
    response = await client.post("/hero/", json=payload)
    assert response.status_code == status_code
    if status_code == status.HTTP_201_CREATED:
        assert payload["opendota_name"] == response.json()["opendota_name"]


@pytest.mark.parametrize(
    "hero_id, params, status_code",
    (
        (
            None,
            {},
            status.HTTP_200_OK,
        ),
        (
            None,
            {
                "include_match_players": 1,
                "include_player_hero_chances": 1
            },
            status.HTTP_200_OK,
        ),
        (
            1,
            {},
            status.HTTP_200_OK,
        ),
        (
            2,
            {},
            status.HTTP_404_NOT_FOUND,
        ),
        (
            1,
            {
                "include_match_players": 1,
                "include_player_hero_chances": 1
            },
            status.HTTP_200_OK,
        ),
    ),
)
async def test_get_hero(client: AsyncClient, hero_id: Optional[int], params: dict, status_code: int):
    response = await client.get(f"/hero/{hero_id if hero_id else ''}", params=params)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "hero_id, payload, status_code",
    (
        (
            1,
            {},
            status.HTTP_200_OK,
        ),
        (
            1,
            {
                "opendota_name": "nevermore"
            },
            status.HTTP_200_OK,
        ),
        (
            2,
            {},
            status.HTTP_404_NOT_FOUND,
        ),
    ),
)
async def test_upd_hero(client: AsyncClient, hero_id: Optional[int], payload: dict, status_code: int):
    response = await client.patch(f"/hero/{hero_id}", json=payload)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "hero_id, status_code",
    (
        (
            1,
            status.HTTP_204_NO_CONTENT,
        ),
        (
            2,
            status.HTTP_404_NOT_FOUND,
        )
    ),
)
async def test_delete_hero(client: AsyncClient, hero_id: Optional[int], status_code: int):
    response = await client.delete(f"/hero/{hero_id}")
    assert response.status_code == status_code
