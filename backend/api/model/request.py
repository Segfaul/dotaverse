from sqlalchemy import String, Integer, DateTime, func
from sqlalchemy.orm import DeclarativeBase as Base, Mapped, mapped_column

from backend.api.model.base import Base
from backend.api.model.mixin import CRUDMixin


class Request(Base, CRUDMixin):
    '''
    API Request info

    Attributes
    ----------
    dotabuff_link : str
        link associated with the request
    status : int
        status of the request
    created_at : datetime
        date the request was created
    '''
    __tablename__ = "request"

    id: Mapped[int] = mapped_column(
        "id", autoincrement=True, nullable=False, unique=True, primary_key=True
    )
    dotabuff_link: Mapped[str] = mapped_column("dotabuff_link", String(length=128), nullable=False)
    status: Mapped[int] = mapped_column("status", Integer, default=200, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        "created_at", DateTime("Europe/Moscow"), 
        default=func.now
    )