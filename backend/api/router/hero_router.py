from typing import List, Optional

from fastapi import APIRouter, Depends, Path, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from backend.config import limiter
from backend.api.service.db_service import get_session
from backend.api.util import get_object_or_raise_404, create_object_or_raise_400, \
    update_object_or_raise_400, auth_admin
from backend.api.model import Hero
from backend.api.schema import HeroSchema, PartialHeroSchema, HeroResponse

router = APIRouter(
    prefix="/v1/hero",
    tags=['Hero']
)

@router.get(
    "/", status_code=status.HTTP_200_OK,
    response_model=List[HeroResponse], response_model_exclude_unset=True
)
@limiter.limit("45/minute")
async def read_all_heroes(
    request: Request,
    include_match_players: Optional[bool] = 0,
    include_player_hero_chances: Optional[bool] = 0,
    db_session: AsyncSession = Depends(get_session)
):
    return [
        HeroResponse(**hero.__dict__).model_dump(exclude_unset=True) \
        async for hero in Hero.read_all(
            db_session,
            **dict(request.query_params)
        )
    ]


@router.get(
    "/{hero_id}", status_code=status.HTTP_200_OK,
    response_model=HeroResponse, response_model_exclude_unset=True
)
@limiter.limit("45/minute")
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
