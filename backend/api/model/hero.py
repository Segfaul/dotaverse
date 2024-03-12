from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase as Base, Mapped, mapped_column

from backend.api.model.base import Base
from backend.api.model.mixin import CRUDMixin


class Hero(Base, CRUDMixin):
    '''
    Dota2 hero

    Attributes
    ----------
    dotabuff_name : str
        name of the hero on Dotabuff
    gif_link : str
        link to the hero's animation
    '''
    __tablename__ = "hero"

    id: Mapped[int] = mapped_column(
        "id", autoincrement=True, nullable=False, unique=True, primary_key=True
    )
    dotabuff_name: Mapped[str] = mapped_column("dotabuff_name", String(length=64), nullable=False)
    gif_link: Mapped[str] = mapped_column("gif_link", String(length=128), nullable=False)
