from typing import Optional, List

from fastapi import APIRouter, Depends, Path, status, Request
# from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.service.db_service import get_session
from backend.api.util import get_object_or_raise_404, create_object_or_raise_400
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


# @router.get(
#     "/{teamplayer_id}/stats", status_code=status.HTTP_200_OK,
#     response_model=TeamPlayerStatsSchema, response_model_exclude_unset=True
# )
# async def read_teamplayer_stats(
#     teamplayer_id: int = Path(...),
#     db_session: AsyncSession = Depends(get_session)
# ):
#     teamplayer = await get_object_or_raise_404(
#         db_session, TeamPlayer, teamplayer_id,
#         joinedload(TeamPlayer.team),
#         joinedload(TeamPlayer.match_teamplayers)
#             .subqueryload(MatchTeamPlayer.match)
#                 .subqueryload(Match.match_teams),
#         joinedload(TeamPlayer.match_teamplayers).subqueryload(MatchTeamPlayer.teamplayer),
#         joinedload(TeamPlayer.match_teamplayers).subqueryload(MatchTeamPlayer.hero),
#         joinedload(TeamPlayer.teamplayer_hero_chances)
#     )
#     return TeamPlayerStatsSchema(**teamplayer.__dict__).model_dump(exclude_unset=True)


@router.post(
    "/", status_code=status.HTTP_201_CREATED,
    response_model=TeamPlayerResponse, response_model_exclude_unset=True
)
async def create_teamplayer(
    payload: TeamPlayerSchema = Depends(), db_session: AsyncSession = Depends(get_session)
):
    teamplayer = await create_object_or_raise_400(db_session, TeamPlayer, **payload.model_dump())
    return TeamPlayerResponse(**teamplayer.__dict__).model_dump(exclude_unset=True)


@router.patch(
    "/{teamplayer_id}", status_code=status.HTTP_200_OK,
    response_model=TeamPlayerResponse, response_model_exclude_unset=True
)
async def update_teamplayer(
    teamplayer_id: int = Path(...), payload: PartialTeamPlayerSchema = Depends(),
    db_session: AsyncSession = Depends(get_session)
):
    teamplayer = await get_object_or_raise_404(db_session, TeamPlayer, teamplayer_id)
    await TeamPlayer.update(db_session, teamplayer, **payload.model_dump())
    return TeamPlayerResponse(**teamplayer.__dict__).model_dump(exclude_unset=True)


@router.delete(
    "/{teamplayer_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_teamplayer(
    teamplayer_id: int = Path(...), db_session: AsyncSession = Depends(get_session)
):
    teamplayer = await get_object_or_raise_404(db_session, TeamPlayer, teamplayer_id)
    await TeamPlayer.delete(db_session, teamplayer)
