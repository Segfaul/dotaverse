from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.service.db_service import get_session
from backend.api.model import Player, PlayerSchema, PlayerResponse

router = APIRouter(
    prefix="/v1/player",
    tags=['Player']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PlayerResponse)
async def create_player(payload: PlayerSchema = Depends(), db_session: AsyncSession = Depends(get_session)):
    return await Player.create(db_session, **payload.model_dump())

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[PlayerResponse])
async def read_all_players(db_session: AsyncSession = Depends(get_session)):
    return [PlayerResponse.model_validate(player) async for player in Player.read_all(db_session)]
