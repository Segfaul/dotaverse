from sqlalchemy import Boolean, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from backend.api.model.base import Base
from backend.api.model.mixin import CRUDMixin


class User(Base, CRUDMixin):
    '''
    Dotaverse User

    Attributes
    ----------
    username : str
        username
    password : str
        hashed password
    is_admin : bool
        does user have admin rights
    created_at : datetime
        date the request was created
    '''
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(
        "id", autoincrement=True, nullable=False, unique=True, primary_key=True
    )
    username: Mapped[str] = mapped_column(
        "username", String(length=64), nullable=False, unique=True
    )
    password: Mapped[str] = mapped_column(
        "password", String(length=255), nullable=False
    )
    is_admin: Mapped[Boolean] = mapped_column("is_admin", Boolean(), default=False, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        "created_at", DateTime("Europe/Moscow"), 
        default=func.now()
    )
