from typing import List

from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.service.db_service import get_session
from backend.api.util import get_object_or_raise_404, create_object_or_raise_400
from backend.api.model import MatchPlayer
from backend.api.schema import MatchPlayerSchema, PartialMatchPlayerSchema, MatchPlayerResponse

router = APIRouter(
    prefix="/v1/matchplayer",
    tags=['MatchPlayer']
)

@router.get(
    "/", status_code=status.HTTP_200_OK,
    response_model=List[MatchPlayerResponse], response_model_exclude_unset=True
)
async def read_all_matchplayers(
    db_session: AsyncSession = Depends(get_session)
):
    return [
        MatchPlayerResponse(**matchplayer.__dict__).model_dump(exclude_unset=True) \
        async for matchplayer in MatchPlayer.read_all(
            db_session
        )
    ]


@router.get(
    "/{matchplayer_id}", status_code=status.HTTP_200_OK,
    response_model=MatchPlayerResponse, response_model_exclude_unset=True
)
async def read_matchplayer(
    matchplayer_id: int = Path(...),
    db_session: AsyncSession = Depends(get_session)
):
    matchplayer = await get_object_or_raise_404(
        db_session, MatchPlayer, matchplayer_id
    )
    return MatchPlayerResponse(**matchplayer.__dict__).model_dump(exclude_unset=True)


@router.post(
    "/", status_code=status.HTTP_201_CREATED,
    response_model=MatchPlayerResponse, response_model_exclude_unset=True
)
async def create_matchplayer(
    payload: MatchPlayerSchema = Depends(), db_session: AsyncSession = Depends(get_session)
):
    matchplayer = await create_object_or_raise_400(db_session, MatchPlayer, **payload.model_dump())
    return MatchPlayerResponse(**matchplayer.__dict__).model_dump(exclude_unset=True)


@router.patch(
    "/{matchplayer_id}", status_code=status.HTTP_200_OK,
    response_model=MatchPlayerResponse, response_model_exclude_unset=True
)
async def update_matchplayer(
    matchplayer_id: int = Path(...), payload: PartialMatchPlayerSchema = Depends(),
    db_session: AsyncSession = Depends(get_session)
):
    matchplayer = await get_object_or_raise_404(db_session, MatchPlayer, matchplayer_id)
    await MatchPlayer.update(db_session, matchplayer, **payload.model_dump())
    return MatchPlayerResponse(**matchplayer.__dict__).model_dump(exclude_unset=True)


@router.delete(
    "/{matchplayer_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_matchplayer(
    matchplayer_id: int = Path(...), db_session: AsyncSession = Depends(get_session)
):
    matchplayer = await get_object_or_raise_404(db_session, MatchPlayer, matchplayer_id)
    await MatchPlayer.delete(db_session, matchplayer)
