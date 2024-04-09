from typing import List

from fastapi import APIRouter, Depends, Path, status, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from backend.config import limiter
from backend.api.service.db_service import get_session
from backend.api.util import get_object_or_raise_404, create_object_or_raise_400, \
    update_object_or_raise_400, auth_admin
from backend.api.model import Match, MatchTeam, MatchPlayer
from backend.api.schema import MatchSchema, PartialMatchSchema, MatchResponse, MatchStatsSchema
from backend.api.schema.stats_schema import IndependentMatchStatsSchema

router = APIRouter(
    prefix="/v1/match",
    tags=['Match']
)


@router.get(
    "/", status_code=status.HTTP_200_OK,
    response_model=List[IndependentMatchStatsSchema], response_model_exclude_unset=True
)
@limiter.limit("45/minute")
async def read_all_matches(
    request: Request,
    db_session: AsyncSession = Depends(get_session)
):
    return [
        IndependentMatchStatsSchema(**match.__dict__).model_dump(exclude_unset=True) \
        async for match in Match.read_all(
            db_session,
            joinedload(Match.match_teams)
                .subqueryload(MatchTeam.team),
            **dict(request.query_params)
        )
    ]


@router.get(
    "/{match_id}", status_code=status.HTTP_200_OK,
    response_model=IndependentMatchStatsSchema, response_model_exclude_unset=True
)
@limiter.limit("45/minute")
async def read_match(
    request: Request,
    match_id: int = Path(...),
    db_session: AsyncSession = Depends(get_session)
):
    match = await get_object_or_raise_404(
        db_session, Match, match_id,
        joinedload(Match.match_teams)
            .subqueryload(MatchTeam.team),
    )
    return IndependentMatchStatsSchema(**match.__dict__).model_dump(exclude_unset=True)


@router.get(
    "/{match_id}/stats", status_code=status.HTTP_200_OK,
    response_model=MatchStatsSchema, response_model_exclude_unset=True
)
@limiter.limit("45/minute")
async def read_match_stats(
    request: Request,
    match_id: int = Path(...),
    db_session: AsyncSession = Depends(get_session)
):
    match = await get_object_or_raise_404(
        db_session, Match, match_id,
        joinedload(Match.match_teams)
            .subqueryload(MatchTeam.team),
        joinedload(Match.match_teams)
            .subqueryload(MatchTeam.match_players)
                .subqueryload(MatchPlayer.hero),
        joinedload(Match.match_teams)
            .subqueryload(MatchTeam.match_players)
                .subqueryload(MatchPlayer.player_hero_chance),
        joinedload(Match.match_teams)
            .subqueryload(MatchTeam.match_players)
                .subqueryload(MatchPlayer.player),
    )
    return MatchStatsSchema(**match.__dict__).model_dump(exclude_unset=True)


@router.post(
    "/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(auth_admin)],
    response_model=MatchResponse, response_model_exclude_unset=True
)
@limiter.limit("45/minute")
async def create_match(
    request: Request,
    payload: MatchSchema, db_session: AsyncSession = Depends(get_session)
):
    match = await create_object_or_raise_400(db_session, Match, **payload.model_dump())
    return MatchResponse(**match.__dict__).model_dump(exclude_unset=True)


@router.post(
    "/calculate", status_code=status.HTTP_201_CREATED,
)
@limiter.limit("45/minute")
async def calculate_match(
    request: Request,
    db_session: AsyncSession = Depends(get_session)
):

    teams = await request.json()
    team_win_chances = {}
    for team_id, players in teams.items():
        win_chance = 1
        for player in players:
            win_chance += player['chosen_phc']['win_percentage']
        win_chance = round(win_chance/5, 4)
        team_win_chances[team_id] = win_chance

    winner_id = max(team_win_chances, key=team_win_chances.get)

    match = await Match.create(db_session)
    match_players: List[MatchPlayer.__dict__] = []
    for team_id, players in teams.items():
        match_team = await MatchTeam.create(
            db_session, team_id=team_id, match_id=match.id, is_winner=(team_id==winner_id)
        )
        player_data: List[MatchPlayer.__dict__] = [
            MatchPlayer(
                player_id=player['id'],
                hero_id=player['chosen_phc']['hero_id'],
                playerherochance_id=player['chosen_phc']['id'],
                matchteam_id=match_team.id,
                match_id=match.id
            ).__dict__ for player in players
        ]
        match_players += player_data

    await db_session.execute(
        MatchPlayer.__table__.insert(),
        match_players
    )
    await db_session.commit()

    return RedirectResponse(f'{match.id}/stats', status_code=status.HTTP_303_SEE_OTHER)


@router.patch(
    "/{match_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(auth_admin)],
    response_model=MatchResponse, response_model_exclude_unset=True
)
@limiter.limit("45/minute")
async def update_match(
    request: Request,
    payload: PartialMatchSchema, match_id: int = Path(...),
    db_session: AsyncSession = Depends(get_session)
):
    match = await get_object_or_raise_404(db_session, Match, match_id)
    await update_object_or_raise_400(db_session, Match, match, **payload.model_dump())
    return MatchResponse(**match.__dict__).model_dump(exclude_unset=True)


@router.delete(
    "/{match_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(auth_admin)]
)
@limiter.limit("45/minute")
async def delete_match(
    request: Request,
    match_id: int = Path(...), db_session: AsyncSession = Depends(get_session)
):
    match = await get_object_or_raise_404(db_session, Match, match_id)
    await Match.delete(db_session, match)
