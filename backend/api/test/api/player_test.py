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
                "name": "Puppey",
                "steamid": 76561198047544485,
                "opendota_link": "https://www.opendota.com/players/87278757"
            },
            status.HTTP_201_CREATED,
        ),
        (
            {
                "name": "Puppey",
                "steamid": 76561198047544485,
                "opendota_link": "https://www.opendota.com/players/87278757"
            },
            status.HTTP_400_BAD_REQUEST,
        ),
        (
            {
                "name": "Puppey",
                "steamid": 765611980475444850,
                "opendota_link": "somefakelink.com/87278757"
            },
            status.HTTP_400_BAD_REQUEST,
        ),
        (
            {
                "name": "Puppey",
                "steamid": 'dude',
                "opendota_link": "https://www.opendota.com/players/87278757"
            },
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        ),
    ),
)
async def test_add_player(client: AsyncClient, payload: dict, status_code: int):
    response = await client.post("/player/", json=payload)
    assert response.status_code == status_code
    if status_code == status.HTTP_201_CREATED:
        assert payload["name"] == response.json()["name"]


@pytest.mark.parametrize(
    "player_id, stats, params, status_code",
    (
        (
            None,
            0,
            {},
            status.HTTP_200_OK,
        ),
        (
            None,
            0,
            {
                "include_team_players": 1,
                "include_match_players": 1,
                "include_player_hero_chances": 1
            },
            status.HTTP_200_OK,
        ),
        (
            1,
            0,
            {},
            status.HTTP_200_OK,
        ),
        (
            1,
            1,
            {},
            status.HTTP_200_OK,
        ),
        (
            2,
            0,
            {},
            status.HTTP_404_NOT_FOUND,
        ),
        (
            2,
            1,
            {},
            status.HTTP_404_NOT_FOUND,
        ),
        (
            1,
            0,
            {
                "include_team_players": 1,
                "include_match_players": 1,
                "include_player_hero_chances": 1
            },
            status.HTTP_200_OK,
        ),
    ),
)
async def test_get_player(client: AsyncClient, player_id: Optional[int], stats: Optional[bool], params: dict, status_code: int):
    response = await client.get(
        f"/player/{player_id if player_id else ''}{'/stats' if stats else ''}",
        params=params
    )
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "player_id, payload, status_code",
    (
        (
            1,
            {},
            status.HTTP_200_OK,
        ),
        (
            1,
            {
                "name": "Puppey"
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
                "steamid": "xxxx"
            },
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        ),
    ),
)
async def test_upd_player(client: AsyncClient, player_id: Optional[int], payload: dict, status_code: int):
    response = await client.patch(f"/player/{player_id}", json=payload)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "player_id, status_code",
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
async def test_delete_player(client: AsyncClient, player_id: Optional[int], status_code: int):
    response = await client.delete(f"/player/{player_id}")
    assert response.status_code == status_code
