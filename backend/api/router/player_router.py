from typing import Optional, List

from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.service.db_service import get_session
from backend.api.util import get_object_or_raise_404, create_object_or_raise_400
from backend.api.model import Player
from backend.api.schema import PlayerSchema, PartialPlayerSchema, PlayerResponse

router = APIRouter(
    prefix="/v1/player",
    tags=['Player']
)


@router.get(
    "/", status_code=status.HTTP_200_OK,
    response_model=List[PlayerResponse], response_model_exclude_unset=True
)
async def read_all_players(
    include_matchplayers: Optional[bool] = 0,
    include_playerherochances: Optional[bool] = 0,
    db_session: AsyncSession = Depends(get_session)
):
    return [
        PlayerResponse(**player.__dict__).model_dump(exclude_unset=True) \
        async for player in Player.read_all(
            db_session,
            include_matchplayers=include_matchplayers,
            include_playerherochances=include_playerherochances,
        )
    ]


@router.get(
    "/{player_id}", status_code=status.HTTP_200_OK,
    response_model=PlayerResponse, response_model_exclude_unset=True
)
async def read_player(
    player_id: int = Path(...),
    include_matchplayers: Optional[bool] = 0,
    include_playerherochances: Optional[bool] = 0,
    db_session: AsyncSession = Depends(get_session)
):
    player = await get_object_or_raise_404(
        db_session, Player, player_id,
        include_matchplayers=include_matchplayers,
        include_playerherochances=include_playerherochances
    )
    return PlayerResponse(**player.__dict__).model_dump(exclude_unset=True)


@router.post(
    "/", status_code=status.HTTP_201_CREATED,
    response_model=PlayerResponse, response_model_exclude_unset=True
)
async def create_player(
    payload: PlayerSchema = Depends(), db_session: AsyncSession = Depends(get_session)
):
    player = await create_object_or_raise_400(db_session, Player, **payload.model_dump())
    return PlayerResponse(**player.__dict__).model_dump(exclude_unset=True)


@router.patch(
    "/{player_id}", status_code=status.HTTP_200_OK,
    response_model=PlayerResponse, response_model_exclude_unset=True
)
async def update_player(
    player_id: int = Path(...), payload: PartialPlayerSchema = Depends(),
    db_session: AsyncSession = Depends(get_session)
):
    player = await get_object_or_raise_404(db_session, Player, player_id)
    await Player.update(db_session, player, **payload.model_dump())
    return PlayerResponse(**player.__dict__).model_dump(exclude_unset=True)


@router.delete(
    "/{player_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_player(
    player_id: int = Path(...), db_session: AsyncSession = Depends(get_session)
):
    player = await get_object_or_raise_404(db_session, Player, player_id)
    await Player.delete(db_session, player)
