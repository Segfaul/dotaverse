from typing import List, Optional

from fastapi import APIRouter, Depends, Path, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.service.db_service import get_session
from backend.api.util import get_object_or_raise_404, create_object_or_raise_400, \
    update_object_or_raise_400
from backend.api.model import MatchTeam
from backend.api.schema import MatchTeamSchema, PartialMatchTeamSchema, MatchTeamResponse

router = APIRouter(
    prefix="/v1/matchteam",
    tags=['MatchTeam']
)

@router.get(
    "/", status_code=status.HTTP_200_OK,
    response_model=List[MatchTeamResponse], response_model_exclude_unset=True
)
async def read_all_matchteams(
    request: Request,
    include_match_players: Optional[bool] = 0,
    db_session: AsyncSession = Depends(get_session)
):
    return [
        MatchTeamResponse(**matchteam.__dict__).model_dump(exclude_unset=True) \
        async for matchteam in MatchTeam.read_all(
            db_session,
            **dict(request.query_params)
        )
    ]


@router.get(
    "/{matchteam_id}", status_code=status.HTTP_200_OK,
    response_model=MatchTeamResponse, response_model_exclude_unset=True
)
async def read_matchteam(
    matchteam_id: int = Path(...),
    include_match_players: Optional[bool] = 0,
    db_session: AsyncSession = Depends(get_session)
):
    matchteam = await get_object_or_raise_404(
        db_session, MatchTeam, matchteam_id,
        include_match_players=include_match_players
    )
    return MatchTeamResponse(**matchteam.__dict__).model_dump(exclude_unset=True)


@router.post(
    "/", status_code=status.HTTP_201_CREATED,
    response_model=MatchTeamResponse, response_model_exclude_unset=True
)
async def create_matchteam(
    payload: MatchTeamSchema = Depends(), db_session: AsyncSession = Depends(get_session)
):
    matchteam = await create_object_or_raise_400(db_session, MatchTeam, **payload.model_dump())
    return MatchTeamResponse(**matchteam.__dict__).model_dump(exclude_unset=True)


@router.patch(
    "/{matchteam_id}", status_code=status.HTTP_200_OK,
    response_model=MatchTeamResponse, response_model_exclude_unset=True
)
async def update_matchteam(
    matchteam_id: int = Path(...), payload: PartialMatchTeamSchema = Depends(),
    db_session: AsyncSession = Depends(get_session)
):
    matchteam = await get_object_or_raise_404(db_session, MatchTeam, matchteam_id)
    await update_object_or_raise_400(db_session, MatchTeam, matchteam, **payload.model_dump())
    return MatchTeamResponse(**matchteam.__dict__).model_dump(exclude_unset=True)


@router.delete(
    "/{matchteam_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_matchteam(
    matchteam_id: int = Path(...), db_session: AsyncSession = Depends(get_session)
):
    matchteam = await get_object_or_raise_404(db_session, MatchTeam, matchteam_id)
    await MatchTeam.delete(db_session, matchteam)
