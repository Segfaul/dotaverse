from fastapi import status, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


async def get_object_or_raise_404(db_session: AsyncSession, item, item_id: int, **kwargs):
    """
    Response pattern for api endpoint if current item doesn't exist
    """
    instance = await item.read_by_id(db_session, item_id, **kwargs)
    if not instance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{item.__name__} not found"
        )
    return instance


async def create_object_or_raise_400(db_session: AsyncSession, item, **kwargs):
    """
    Response pattern for api endpoint if inegrity error occured (FK)
    """
    try:
        instance = await item.create(db_session, **kwargs)
        return instance
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"[{item.__name__}] Foreign key constraint violated: " + str(e.__cause__)
        ) from e

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"[{item.__name__}] Internal server error: " + str(e.__cause__)
        ) from e
