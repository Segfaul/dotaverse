from typing import List, Optional

from fastapi import APIRouter, Depends, Path, status, Request
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from backend.config import limiter
from backend.api.service.db_service import get_session
from backend.api.util import get_object_or_raise_404, create_object_or_raise_400, \
    update_object_or_raise_400, auth_admin, process_query_params, cache
from backend.api.model import Hero, PlayerHeroChance, MatchPlayer, Match, MatchTeam
from backend.api.schema import HeroSchema, PartialHeroSchema, HeroResponse, \
    IndependentHeroStatsSchema

router = APIRouter(
    prefix="/v1/hero",
    tags=['Hero']
)

@router.get(
    "/", status_code=status.HTTP_200_OK,
    response_model=List[HeroResponse], response_model_exclude_unset=True
)
@limiter.limit("45/minute")
@cache(expire=3600)
async def read_all_heroes(
    request: Request,
    db_session: AsyncSession = Depends(get_session)
):
    query_params: dict = process_query_params(request)
    return [
        HeroResponse(**hero.__dict__).model_dump(exclude_unset=True) \
        async for hero in Hero.read_all(
            db_session,
            **query_params
        )
    ]


@router.get(
    "/{hero_id}", status_code=status.HTTP_200_OK,
    response_model=HeroResponse, response_model_exclude_unset=True
)
@limiter.limit("45/minute")
@cache(expire=300)
async def read_hero(
    request: Request,
    hero_id: int = Path(...),
    include_match_players: Optional[bool] = 0,
    include_player_hero_chances: Optional[bool] = 0,
    db_session: AsyncSession = Depends(get_session)
):
    hero = await get_object_or_raise_404(
        db_session, Hero, hero_id,
        include_match_players=include_match_players,
        include_player_hero_chances=include_player_hero_chances
    )
    return HeroResponse(**hero.__dict__).model_dump(exclude_unset=True)


@router.get(
    "/{hero_id}/stats", status_code=status.HTTP_200_OK,
    response_model=IndependentHeroStatsSchema, response_model_exclude_unset=True
)
@limiter.limit("45/minute")
@cache(expire=150)
async def read_hero_stats(
    request: Request,
    hero_id: int = Path(...),
    db_session: AsyncSession = Depends(get_session)
):
    hero = await get_object_or_raise_404(
        db_session, Hero, hero_id,
        joinedload(Hero.player_hero_chances)
            .subqueryload(PlayerHeroChance.player),
        joinedload(Hero.player_hero_chances)
            .subqueryload(PlayerHeroChance.match_players)
                .subqueryload(MatchPlayer.match)
                    .subqueryload(Match.match_teams)
                        .subqueryload(MatchTeam.team)
    )
    return IndependentHeroStatsSchema(**hero.__dict__).model_dump(exclude_unset=True)


@router.post(
    "/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(auth_admin)],
    response_model=HeroResponse, response_model_exclude_unset=True
)
@limiter.limit("45/minute")
async def create_hero(
    request: Request,
    payload: HeroSchema, db_session: AsyncSession = Depends(get_session)
):
    hero = await create_object_or_raise_400(db_session, Hero, **payload.model_dump())
    return HeroResponse(**hero.__dict__).model_dump(exclude_unset=True)


@router.patch(
    "/{hero_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(auth_admin)],
    response_model=HeroResponse, response_model_exclude_unset=True
)
@limiter.limit("45/minute")
async def update_hero(
    request: Request,
    payload: PartialHeroSchema, hero_id: int = Path(...),
    db_session: AsyncSession = Depends(get_session)
):
    hero = await get_object_or_raise_404(db_session, Hero, hero_id)
    await update_object_or_raise_400(db_session, Hero, hero, **payload.model_dump())
    return HeroResponse(**hero.__dict__).model_dump(exclude_unset=True)


@router.delete(
    "/{hero_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(auth_admin)],
)
@limiter.limit("45/minute")
async def delete_hero(
    request: Request,
    hero_id: int = Path(...), db_session: AsyncSession = Depends(get_session)
):
    hero = await get_object_or_raise_404(db_session, Hero, hero_id)
    await Hero.delete(db_session, hero)
