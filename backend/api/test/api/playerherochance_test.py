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
                "player_id": 1,
                "hero_id": 1,
                "win_percentage": 20.58
            },
            status.HTTP_201_CREATED,
        ),
        (
            {
                "player_id": 1,
                "hero_id": 1,
                "win_percentage": "some_percentage"
            },
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        ),
    ),
)
async def test_add_playerherochance(client: AsyncClient, payload: dict, status_code: int):
    response = await client.post("/playerherochance/", params=payload)
    assert response.status_code == status_code
    if status_code == status.HTTP_201_CREATED:
        assert payload["win_percentage"] == response.json()["win_percentage"]


@pytest.mark.parametrize(
    "playerherochance_id, payload, status_code",
    (
        (
            None,
            {},
            status.HTTP_200_OK,
        ),
        (
            None,
            {
                "include_match_players": 1
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
                "include_match_players": 1
            },
            status.HTTP_200_OK,
        ),
    ),
)
async def test_get_playeherochance(client: AsyncClient, playerherochance_id: Optional[int], payload: dict, status_code: int):
    response = await client.get(
        f"/playerherochance/{playerherochance_id if playerherochance_id else ''}",
        params=payload
    )
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "playerherochance_id, payload, status_code",
    (
        (
            1,
            {},
            status.HTTP_200_OK,
        ),
        (
            1,
            {
                "player_id": 1
            },
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
                "player_id": "some player_id"
            },
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        ),
    ),
)
async def test_upd_playeherochance(client: AsyncClient, playerherochance_id: Optional[int], payload: dict, status_code: int):
    response = await client.patch(f"/playerherochance/{playerherochance_id}", params=payload)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "playerherochance_id, status_code",
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
async def test_delete_team(client: AsyncClient, playerherochance_id: Optional[int], status_code: int):
    response = await client.delete(f"/playerherochance/{playerherochance_id}")
    assert response.status_code == status_code