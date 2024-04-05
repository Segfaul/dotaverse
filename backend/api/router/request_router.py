from typing import List

from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.service.db_service import get_session
from backend.api.util import get_object_or_raise_404, create_object_or_raise_400, \
    update_object_or_raise_400
from backend.api.model import Request
from backend.api.schema import RequestSchema, PartialRequestSchema, RequestResponse

router = APIRouter(
    prefix="/v1/request",
    tags=['Request']
)

@router.get(
    "/", status_code=status.HTTP_200_OK,
    response_model=List[RequestResponse], response_model_exclude_unset=True
)
async def read_all_requests(
    db_session: AsyncSession = Depends(get_session)
):
    return [
        RequestResponse(**request.__dict__).model_dump(exclude_unset=True) \
        async for request in Request.read_all(
            db_session,
        )
    ]


@router.get(
    "/{request_id}", status_code=status.HTTP_200_OK,
    response_model=RequestResponse, response_model_exclude_unset=True
)
async def read_request(
    request_id: int = Path(...),
    db_session: AsyncSession = Depends(get_session)
):
    request = await get_object_or_raise_404(
        db_session, Request, request_id
    )
    return RequestResponse(**request.__dict__).model_dump(exclude_unset=True)


@router.post(
    "/", status_code=status.HTTP_201_CREATED,
    response_model=RequestResponse, response_model_exclude_unset=True
)
async def create_request(
    payload: RequestSchema, db_session: AsyncSession = Depends(get_session)
):
    request = await create_object_or_raise_400(db_session, Request, **payload.model_dump())
    return RequestResponse(**request.__dict__).model_dump(exclude_unset=True)


@router.patch(
    "/{request_id}", status_code=status.HTTP_200_OK,
    response_model=RequestResponse, response_model_exclude_unset=True
)
async def update_request(
    payload: PartialRequestSchema, request_id: int = Path(...),
    db_session: AsyncSession = Depends(get_session)
):
    request = await get_object_or_raise_404(db_session, Request, request_id)
    await update_object_or_raise_400(db_session, Request, request, **payload.model_dump())
    return RequestResponse(**request.__dict__).model_dump(exclude_unset=True)


@router.delete(
    "/{request_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_request(
    request_id: int = Path(...), db_session: AsyncSession = Depends(get_session)
):
    request = await get_object_or_raise_404(db_session, Request, request_id)
    await Request.delete(db_session, request)
