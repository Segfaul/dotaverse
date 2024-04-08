from datetime import timedelta
from typing import List, Annotated

from fastapi import APIRouter, Depends, Path, status, Request, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.service.db_service import get_session
from backend.api.util import get_object_or_raise_404, create_object_or_raise_400, \
    update_object_or_raise_400, \
    get_password_hash, authenticate_user, create_access_token, \
    ACCESS_TOKEN_EXPIRE_MINUTES, auth_user, auth_admin
from backend.api.model import User
from backend.api.schema import UserSchema, PartialUserSchema, UserResponse, TokenSchema

router = APIRouter(
    prefix="/v1/user",
    tags=['User']
)


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db_session: AsyncSession = Depends(get_session)
) -> TokenSchema:
    user = await authenticate_user(
        db_session, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"user_id": user.id, "username": user.username, "is_admin": user.is_admin},
        expires_delta=access_token_expires
    )
    return TokenSchema(access_token=access_token, token_type="bearer")


@router.get(
    "/", status_code=status.HTTP_200_OK, dependencies=[Depends(auth_admin)],
    response_model=List[UserResponse], response_model_exclude_unset=True
)
async def read_all_users(
    request: Request,
    db_session: AsyncSession = Depends(get_session)
):
    return [
        UserResponse(**user.__dict__).model_dump(exclude_unset=True) \
        async for user in User.read_all(
            db_session,
            **dict(request.query_params)
        )
    ]


@router.get(
    "/me", status_code=status.HTTP_200_OK,
    response_model=UserResponse, response_model_exclude_unset=True
)
async def read_user_me(
    current_user: Annotated[UserSchema, Depends(auth_user)]
):
    return current_user


@router.get(
    "/{user_id}", status_code=status.HTTP_200_OK,
    response_model=UserResponse, response_model_exclude_unset=True
)
async def read_user(
    current_user: Annotated[UserSchema, Depends(auth_user)],
    user_id: int = Path(...),
    db_session: AsyncSession = Depends(get_session)
):
    if (user.id == current_user['id']) or current_user['is_admin']:
        user = await get_object_or_raise_404(
            db_session, User, user_id,
        )
        return UserResponse(**user.__dict__).model_dump(exclude_unset=True)

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Not enough permissions"
    )


@router.post(
    "/register", status_code=status.HTTP_201_CREATED,
    response_model=UserResponse, response_model_exclude_unset=True
)
async def create_user(
    payload: UserSchema, db_session: AsyncSession = Depends(get_session)
):
    payload.password = await get_password_hash(payload.password)
    user = await create_object_or_raise_400(db_session, User, **payload.model_dump())
    return UserResponse(**user.__dict__).model_dump(exclude_unset=True)


@router.patch(
    "/{user_id}", status_code=status.HTTP_200_OK,
    response_model=UserResponse, response_model_exclude_unset=True
)
async def update_user(
    payload: PartialUserSchema,
    current_user: Annotated[UserSchema, Depends(auth_user)],
    user_id: int = Path(...),
    db_session: AsyncSession = Depends(get_session)
):
    user = await get_object_or_raise_404(db_session, User, user_id)
    if (user.id == current_user['id'] and payload.is_admin is None) or current_user['is_admin']:
        if payload.password:
            payload.password = await get_password_hash(payload.password)
        await update_object_or_raise_400(db_session, User, user, **payload.model_dump())
        return UserResponse(**user.__dict__).model_dump(exclude_unset=True)

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Not enough permissions"
    )


@router.delete(
    "/{user_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_user(
    current_user: Annotated[UserSchema, Depends(auth_user)],
    user_id: int = Path(...), db_session: AsyncSession = Depends(get_session)
):
    if (user.id == current_user['id']) or current_user['is_admin']:
        user = await get_object_or_raise_404(db_session, User, user_id)
        await User.delete(db_session, user)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
