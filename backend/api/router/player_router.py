from typing import Optional, List

from fastapi import APIRouter, Depends, Path, status, Request
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.service.db_service import get_session
from backend.api.util import get_object_or_raise_404, create_object_or_raise_400, \
    update_object_or_raise_400
from backend.api.model import Player, Match, MatchPlayer, TeamPlayer, MatchTeam, PlayerHeroChance
from backend.api.schema import PlayerSchema, PartialPlayerSchema, PlayerResponse, PlayerStatsSchema

router = APIRouter(
    prefix="/v1/player",
    tags=['Player']
)


@router.get(
    "/", status_code=status.HTTP_200_OK,
    response_model=List[PlayerResponse], response_model_exclude_unset=True
)
async def read_all_players(
    request: Request,
    include_team_players: Optional[bool] = 0,
    include_match_players: Optional[bool] = 0,
    include_player_hero_chances: Optional[bool] = 0,
    db_session: AsyncSession = Depends(get_session)
):
    return [
        PlayerResponse(**player.__dict__).model_dump(exclude_unset=True) \
        async for player in Player.read_all(
            db_session,
            **dict(request.query_params)
        )
    ]


@router.get(
    "/{player_id}", status_code=status.HTTP_200_OK,
    response_model=PlayerResponse, response_model_exclude_unset=True
)
async def read_player(
    player_id: int = Path(...),
    include_team_players: Optional[bool] = 0,
    include_match_players: Optional[bool] = 0,
    include_player_hero_chances: Optional[bool] = 0,
    db_session: AsyncSession = Depends(get_session)
):
    player = await get_object_or_raise_404(
        db_session, Player, player_id,
        include_team_players=include_team_players,
        include_match_players=include_match_players,
        include_player_hero_chances=include_player_hero_chances
    )
    return PlayerResponse(**player.__dict__).model_dump(exclude_unset=True)


@router.get(
    "/{player_id}/stats", status_code=status.HTTP_200_OK,
    response_model=PlayerStatsSchema, response_model_exclude_unset=True
)
async def read_player_stats(
    player_id: int = Path(...),
    db_session: AsyncSession = Depends(get_session)
):
    player = await get_object_or_raise_404(
        db_session, Player, player_id,
        joinedload(Player.team_players)
            .subqueryload(TeamPlayer.team),
        joinedload(Player.match_players)
            .subqueryload(MatchPlayer.match)
                .subqueryload(Match.match_teams)
                    .subqueryload(MatchTeam.team),
        joinedload(Player.match_players).subqueryload(MatchPlayer.player),
        joinedload(Player.match_players).subqueryload(MatchPlayer.hero),
        joinedload(Player.player_hero_chances).subqueryload(PlayerHeroChance.hero)
    )
    return PlayerStatsSchema(**player.__dict__).model_dump(exclude_unset=True)


@router.post(
    "/", status_code=status.HTTP_201_CREATED,
    response_model=PlayerResponse, response_model_exclude_unset=True
)
async def create_player(
    payload: PlayerSchema, db_session: AsyncSession = Depends(get_session)
):
    player = await create_object_or_raise_400(db_session, Player, **payload.model_dump())
    return PlayerResponse(**player.__dict__).model_dump(exclude_unset=True)


@router.patch(
    "/{player_id}", status_code=status.HTTP_200_OK,
    response_model=PlayerResponse, response_model_exclude_unset=True
)
async def update_player(
    payload: PartialPlayerSchema, player_id: int = Path(...),
    db_session: AsyncSession = Depends(get_session)
):
    player = await get_object_or_raise_404(db_session, Player, player_id)
    await update_object_or_raise_400(db_session, Player, player, **payload.model_dump())
    return PlayerResponse(**player.__dict__).model_dump(exclude_unset=True)


@router.delete(
    "/{player_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_player(
    player_id: int = Path(...), db_session: AsyncSession = Depends(get_session)
):
    player = await get_object_or_raise_404(db_session, Player, player_id)
    await Player.delete(db_session, player)
