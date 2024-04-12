from typing import List, Optional

from fastapi import APIRouter, Depends, Path, status, Request
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from backend.config import limiter
from backend.api.service.db_service import get_session
from backend.api.util import get_object_or_raise_404, create_object_or_raise_400, \
    update_object_or_raise_400, auth_admin, process_query_params, cache
from backend.api.model import Team, Player, TeamPlayer, PlayerHeroChance, Match, MatchTeam
from backend.api.schema import TeamSchema, PartialTeamSchema, TeamResponse, TeamStatsSchema

router = APIRouter(
    prefix="/v1/team",
    tags=['Team']
)

@router.get(
    "/", status_code=status.HTTP_200_OK,
    response_model=List[TeamResponse], response_model_exclude_unset=True
)
@limiter.limit("45/minute")
@cache(expire=3600)
async def read_all_teams(
    request: Request,
    db_session: AsyncSession = Depends(get_session)
):
    query_params: dict = process_query_params(request)
    return [
        TeamResponse(**team.__dict__).model_dump(exclude_unset=True) \
        async for team in Team.read_all(
            db_session,
            **query_params
        )
    ]


@router.get(
    "/{team_id}", status_code=status.HTTP_200_OK,
    response_model=TeamResponse, response_model_exclude_unset=True
)
@limiter.limit("45/minute")
@cache(expire=150)
async def read_team(
    request: Request,
    team_id: int = Path(...),
    include_team_players: Optional[bool] = 0,
    include_match_teams: Optional[bool] = 0,
    db_session: AsyncSession = Depends(get_session)
):
    team = await get_object_or_raise_404(
        db_session, Team, team_id,
        include_team_players=include_team_players, include_match_teams=include_match_teams
    )
    return TeamResponse(**team.__dict__).model_dump(exclude_unset=True)


@router.get(
    "/{team_id}/stats", status_code=status.HTTP_200_OK,
    response_model=TeamStatsSchema, response_model_exclude_unset=True
)
@limiter.limit("45/minute")
@cache(expire=150)
async def read_team_stats(
    request: Request,
    team_id: int = Path(...),
    db_session: AsyncSession = Depends(get_session)
):
    team = await get_object_or_raise_404(
        db_session, Team, team_id,
        joinedload(Team.team_players)
            .subqueryload(TeamPlayer.player)
                .subqueryload(Player.player_hero_chances)
                    .subqueryload(PlayerHeroChance.hero),
        joinedload(Team.match_teams)
            .subqueryload(MatchTeam.match)
                .subqueryload(Match.match_teams)
                    .subqueryload(MatchTeam.team)
    )
    return TeamStatsSchema(**team.__dict__).model_dump(exclude_unset=True)


@router.post(
    "/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(auth_admin)],
    response_model=TeamResponse, response_model_exclude_unset=True
)
@limiter.limit("45/minute")
async def create_team(
    request: Request,
    payload: TeamSchema, db_session: AsyncSession = Depends(get_session)
):
    team = await create_object_or_raise_400(db_session, Team, **payload.model_dump())
    return TeamResponse(**team.__dict__).model_dump(exclude_unset=True)


@router.patch(
    "/{team_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(auth_admin)],
    response_model=TeamResponse, response_model_exclude_unset=True
)
@limiter.limit("45/minute")
async def update_team(
    request: Request,
    payload: PartialTeamSchema, team_id: int = Path(...),
    db_session: AsyncSession = Depends(get_session)
):
    team = await get_object_or_raise_404(db_session, Team, team_id)
    await update_object_or_raise_400(db_session, Team, team, **payload.model_dump())
    return TeamResponse(**team.__dict__).model_dump(exclude_unset=True)


@router.delete(
    "/{team_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(auth_admin)]
)
@limiter.limit("45/minute")
async def delete_team(
    request: Request,
    team_id: int = Path(...), db_session: AsyncSession = Depends(get_session)
):
    team = await get_object_or_raise_404(db_session, Team, team_id)
    await Team.delete(db_session, team)
