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
                "name": "Team Secret",
                "opendota_link": "https://www.opendota.com/teams/1838315"
            },
            status.HTTP_201_CREATED,
        ),
        (
            {
                "name": "Team Secret",
                "opendota_link": "https://www.opendota.com/teams/1838315"
            },
            status.HTTP_400_BAD_REQUEST,
        ),
        (
            {
                "name": "Team Newbies",
                "opendota_link": "somefakelink.com/1838315"
            },
            status.HTTP_400_BAD_REQUEST,
        ),
        (
            {
                "name": "Team Secret",
                "opendota_link": 12
            },
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        ),
    ),
)
async def test_add_team(
    client: AsyncClient, admin_token: str,
    payload: dict, status_code: int
):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await client.post("/team/", json=payload, headers=headers)
    assert response.status_code == status_code
    if status_code == status.HTTP_201_CREATED:
        assert payload["name"] == response.json()["name"]


@pytest.mark.parametrize(
    "team_id, stats, params, status_code",
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
                "include_match_teams": 1
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
                "include_match_teams": 1
            },
            status.HTTP_200_OK,
        ),
    ),
)
async def test_get_team(
    client: AsyncClient,
    team_id: Optional[int], stats: Optional[bool], params: dict, status_code: int
):
    response = await client.get(
        f"/team/{team_id if team_id else ''}{'/stats' if stats else ''}",
        params=params
    )
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "team_id, payload, status_code",
    (
        (
            1,
            {},
            status.HTTP_200_OK,
        ),
        (
            1,
            {
                "name": "Team Secret"
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
                "opendota_link": 1234
            },
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        ),
    ),
)
async def test_upd_team(
    client: AsyncClient, admin_token: str,
    team_id: Optional[int], payload: dict, status_code: int
):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await client.patch(f"/team/{team_id}", json=payload, headers=headers)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "team_id, status_code",
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
async def test_delete_team(
    client: AsyncClient, admin_token: str,
    team_id: Optional[int], status_code: int
):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await client.delete(f"/team/{team_id}", headers=headers)
    assert response.status_code == status_code
