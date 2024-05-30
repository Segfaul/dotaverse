from typing import List

from fastapi import APIRouter, Depends, status, Request

from backend.api.schema import LogSchema
from backend.api.util import process_query_params, parse_logs, \
    auth_admin, cache

router = APIRouter(
    prefix="/v1/log",
    tags=['Log']
)

@router.get(
    "/", status_code=status.HTTP_200_OK, dependencies=[Depends(auth_admin)],
    response_model=List[LogSchema], response_model_exclude_unset=True
)
@cache(expire=150)
async def get_logs(request: Request):
    query_params: dict = process_query_params(request)
    logs = await parse_logs(**query_params)
    return [
        LogSchema(**log_row).model_dump(exclude_unset=True) \
        for index, log_row in logs.items()
    ]
