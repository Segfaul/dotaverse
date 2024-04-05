from typing import List, Optional

from fastapi import APIRouter, Depends, Path, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.service.db_service import get_session
from backend.api.util import get_object_or_raise_404, create_object_or_raise_400, \
    update_object_or_raise_400
from backend.api.model import PlayerHeroChance
from backend.api.schema import PlayerHeroChanceSchema, PartialPlayerHeroChanceSchema, PlayerHeroChanceResponse

router = APIRouter(
    prefix="/v1/playerherochance",
    tags=['PlayerHeroChance']
)

@router.get(
    "/", status_code=status.HTTP_200_OK,
    response_model=List[PlayerHeroChanceResponse], response_model_exclude_unset=True
)
async def read_all_playerherochances(
    request: Request,
    include_match_players: Optional[bool] = 0,
    db_session: AsyncSession = Depends(get_session)
):
    return [
        PlayerHeroChanceResponse(**playerherochance.__dict__).model_dump(exclude_unset=True) \
        async for playerherochance in PlayerHeroChance.read_all(
            db_session,
            **dict(request.query_params)
        )
    ]


@router.get(
    "/{playerherochance_id}", status_code=status.HTTP_200_OK,
    response_model=PlayerHeroChanceResponse, response_model_exclude_unset=True
)
async def read_playerherochance(
    playerherochance_id: int = Path(...),
    include_match_players: Optional[bool] = 0,
    db_session: AsyncSession = Depends(get_session)
):
    playerherochance = await get_object_or_raise_404(
        db_session, PlayerHeroChance, playerherochance_id,
        include_match_players=include_match_players
    )
    return PlayerHeroChanceResponse(**playerherochance.__dict__).model_dump(exclude_unset=True)


@router.post(
    "/", status_code=status.HTTP_201_CREATED,
    response_model=PlayerHeroChanceResponse, response_model_exclude_unset=True
)
async def create_playerherochance(
    payload: PlayerHeroChanceSchema, db_session: AsyncSession = Depends(get_session)
):
    playerherochance = await create_object_or_raise_400(
        db_session, PlayerHeroChance, **payload.model_dump()
    )
    return PlayerHeroChanceResponse(**playerherochance.__dict__).model_dump(exclude_unset=True)


@router.patch(
    "/{playerherochance_id}", status_code=status.HTTP_200_OK,
    response_model=PlayerHeroChanceResponse, response_model_exclude_unset=True
)
async def update_playerherochance(
    payload: PartialPlayerHeroChanceSchema, playerherochance_id: int = Path(...),
    db_session: AsyncSession = Depends(get_session)
):
    playerherochance = await get_object_or_raise_404(
        db_session, PlayerHeroChance, playerherochance_id
    )
    await update_object_or_raise_400(
        db_session, PlayerHeroChance, playerherochance, **payload.model_dump()
    )
    return PlayerHeroChanceResponse(**playerherochance.__dict__).model_dump(exclude_unset=True)


@router.delete(
    "/{playerherochance_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_playerherochance(
    playerherochance_id: int = Path(...), db_session: AsyncSession = Depends(get_session)
):
    playerherochance = await get_object_or_raise_404(
        db_session, PlayerHeroChance, playerherochance_id
    )
    await PlayerHeroChance.delete(db_session, playerherochance)
