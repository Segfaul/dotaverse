from typing import List

from fastapi import APIRouter, Depends, Path, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.service.db_service import get_session
from backend.api.util import get_object_or_raise_404, create_object_or_raise_400, \
    update_object_or_raise_400, auth_admin
from backend.api.model import TeamPlayer
from backend.api.schema import TeamPlayerSchema, PartialTeamPlayerSchema, TeamPlayerResponse

router = APIRouter(
    prefix="/v1/teamplayer",
    tags=['TeamPlayer']
)


@router.get(
    "/", status_code=status.HTTP_200_OK,
    response_model=List[TeamPlayerResponse], response_model_exclude_unset=True
)
async def read_all_teamplayers(
    request: Request,
    db_session: AsyncSession = Depends(get_session)
):
    return [
        TeamPlayerResponse(**teamplayer.__dict__).model_dump(exclude_unset=True) \
        async for teamplayer in TeamPlayer.read_all(
            db_session,
            **dict(request.query_params)
        )
    ]


@router.get(
    "/{teamplayer_id}", status_code=status.HTTP_200_OK,
    response_model=TeamPlayerResponse, response_model_exclude_unset=True
)
async def read_teamplayer(
    teamplayer_id: int = Path(...),
    db_session: AsyncSession = Depends(get_session)
):
    teamplayer = await get_object_or_raise_404(
        db_session, TeamPlayer, teamplayer_id
    )
    return TeamPlayerResponse(**teamplayer.__dict__).model_dump(exclude_unset=True)


@router.post(
    "/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(auth_admin)],
    response_model=TeamPlayerResponse, response_model_exclude_unset=True
)
async def create_teamplayer(
    payload: TeamPlayerSchema, db_session: AsyncSession = Depends(get_session)
):
    teamplayer = await create_object_or_raise_400(db_session, TeamPlayer, **payload.model_dump())
    return TeamPlayerResponse(**teamplayer.__dict__).model_dump(exclude_unset=True)


@router.patch(
    "/{teamplayer_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(auth_admin)],
    response_model=TeamPlayerResponse, response_model_exclude_unset=True
)
async def update_teamplayer(
    payload: PartialTeamPlayerSchema, teamplayer_id: int = Path(...),
    db_session: AsyncSession = Depends(get_session)
):
    teamplayer = await get_object_or_raise_404(db_session, TeamPlayer, teamplayer_id)
    await update_object_or_raise_400(db_session, TeamPlayer, teamplayer, **payload.model_dump())
    return TeamPlayerResponse(**teamplayer.__dict__).model_dump(exclude_unset=True)


@router.delete(
    "/{teamplayer_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(auth_admin)]
)
async def delete_teamplayer(
    teamplayer_id: int = Path(...), db_session: AsyncSession = Depends(get_session)
):
    teamplayer = await get_object_or_raise_404(db_session, TeamPlayer, teamplayer_id)
    await TeamPlayer.delete(db_session, teamplayer)
