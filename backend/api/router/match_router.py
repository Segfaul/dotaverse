from typing import List, Optional

from fastapi import APIRouter, Depends, Path, status, Request
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.service.db_service import get_session
from backend.api.util import get_object_or_raise_404, create_object_or_raise_400
from backend.api.model import Match, MatchTeam, MatchPlayer
from backend.api.schema import MatchSchema, PartialMatchSchema, MatchResponse, MatchStatsSchema

router = APIRouter(
    prefix="/v1/match",
    tags=['Match']
)

@router.get(
    "/", status_code=status.HTTP_200_OK,
    response_model=List[MatchResponse], response_model_exclude_unset=True
)
async def read_all_matches(
    request: Request,
    include_match_teams: Optional[bool] = 0,
    db_session: AsyncSession = Depends(get_session)
):
    return [
        MatchResponse(**match.__dict__).model_dump(exclude_unset=True) \
        async for match in Match.read_all(
            db_session,
            **dict(request.query_params)
        )
    ]


@router.get(
    "/{match_id}", status_code=status.HTTP_200_OK,
    response_model=MatchResponse, response_model_exclude_unset=True
)
async def read_match(
    match_id: int = Path(...),
    include_match_teams: Optional[bool] = 0,
    db_session: AsyncSession = Depends(get_session)
):
    match = await get_object_or_raise_404(
        db_session, Match, match_id,
        include_match_teams=include_match_teams
    )
    return MatchResponse(**match.__dict__).model_dump(exclude_unset=True)


@router.get(
    "/{match_id}/stats", status_code=status.HTTP_200_OK,
    response_model=MatchStatsSchema, response_model_exclude_unset=True
)
async def read_match_stats(
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
    "/", status_code=status.HTTP_201_CREATED,
    response_model=MatchResponse, response_model_exclude_unset=True
)
async def create_match(
    payload: MatchSchema = Depends(), db_session: AsyncSession = Depends(get_session)
):
    match = await create_object_or_raise_400(db_session, Match, **payload.model_dump())
    return MatchResponse(**match.__dict__).model_dump(exclude_unset=True)


@router.patch(
    "/{match_id}", status_code=status.HTTP_200_OK,
    response_model=MatchResponse, response_model_exclude_unset=True
)
async def update_match(
    match_id: int = Path(...), payload: PartialMatchSchema = Depends(),
    db_session: AsyncSession = Depends(get_session)
):
    match = await get_object_or_raise_404(db_session, Match, match_id)
    await Match.update(db_session, match, **payload.model_dump())
    return MatchResponse(**match.__dict__).model_dump(exclude_unset=True)


@router.delete(
    "/{match_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_match(
    match_id: int = Path(...), db_session: AsyncSession = Depends(get_session)
):
    match = await get_object_or_raise_404(db_session, Match, match_id)
    await Match.delete(db_session, match)
