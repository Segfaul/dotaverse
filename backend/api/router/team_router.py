from typing import List, Optional

from fastapi import APIRouter, Depends, Path, status, Request
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.service.db_service import get_session
from backend.api.util import get_object_or_raise_404, create_object_or_raise_400
from backend.api.model import Team, Player, PlayerHeroChance, MatchTeam
from backend.api.schema import TeamSchema, PartialTeamSchema, TeamResponse, TeamStatsSchema

router = APIRouter(
    prefix="/v1/team",
    tags=['Team']
)

@router.get(
    "/", status_code=status.HTTP_200_OK,
    response_model=List[TeamResponse], response_model_exclude_unset=True
)
async def read_all_teams(
    request: Request,
    include_players: Optional[bool] = 0,
    include_match_teams: Optional[bool] = 0,
    db_session: AsyncSession = Depends(get_session)
):
    return [
        TeamResponse(**team.__dict__).model_dump(exclude_unset=True) \
        async for team in Team.read_all(
            db_session,
            **dict(request.query_params)
        )
    ]


@router.get(
    "/{team_id}", status_code=status.HTTP_200_OK,
    response_model=TeamResponse, response_model_exclude_unset=True
)
async def read_team(
    team_id: int = Path(...),
    include_players: Optional[bool] = 0,
    include_match_teams: Optional[bool] = 0,
    db_session: AsyncSession = Depends(get_session)
):
    team = await get_object_or_raise_404(
        db_session, Team, team_id,
        include_players=include_players, include_match_teams=include_match_teams
    )
    return TeamResponse(**team.__dict__).model_dump(exclude_unset=True)


@router.get(
    "/{team_id}/stats", status_code=status.HTTP_200_OK,
    response_model=TeamStatsSchema, response_model_exclude_unset=True
)
async def read_team_stats(
    team_id: int = Path(...),
    db_session: AsyncSession = Depends(get_session)
):
    team = await get_object_or_raise_404(
        db_session, Team, team_id,
        joinedload(Team.players)
            .subqueryload(Player.player_hero_chances)
                .subqueryload(PlayerHeroChance.hero),
        joinedload(Team.players).subqueryload(Player.match_players),
        joinedload(Team.match_teams).subqueryload(MatchTeam.match)
    )
    return TeamStatsSchema(**team.__dict__).model_dump(exclude_unset=True)


@router.post(
    "/", status_code=status.HTTP_201_CREATED,
    response_model=TeamResponse, response_model_exclude_unset=True
)
async def create_team(
    payload: TeamSchema = Depends(), db_session: AsyncSession = Depends(get_session)
):
    team = await create_object_or_raise_400(db_session, Team, **payload.model_dump())
    return TeamResponse(**team.__dict__).model_dump(exclude_unset=True)


@router.patch(
    "/{team_id}", status_code=status.HTTP_200_OK,
    response_model=TeamResponse, response_model_exclude_unset=True
)
async def update_team(
    team_id: int = Path(...), payload: PartialTeamSchema = Depends(),
    db_session: AsyncSession = Depends(get_session)
):
    team = await get_object_or_raise_404(db_session, Team, team_id)
    await Team.update(db_session, team, **payload.model_dump())
    return TeamResponse(**team.__dict__).model_dump(exclude_unset=True)


@router.delete(
    "/{team_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_team(
    team_id: int = Path(...), db_session: AsyncSession = Depends(get_session)
):
    team = await get_object_or_raise_404(db_session, Team, team_id)
    await Team.delete(db_session, team)
