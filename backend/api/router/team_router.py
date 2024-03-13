from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.service.db_service import get_session
from backend.api.model import Team, TeamSchema, TeamResponse

router = APIRouter(
    prefix="/v1/team",
    tags=['Team']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TeamResponse)
async def create_team(payload: TeamSchema = Depends(), db_session: AsyncSession = Depends(get_session)):
    return await Team.create(db_session, **payload.model_dump())

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[TeamResponse])
async def read_all_teams(db_session: AsyncSession = Depends(get_session)):
    return [TeamResponse.model_validate(team) async for team in Team.read_all(db_session, include_players=True)]
