from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from backend.api.util import _AllOptionalMeta


class UserSchema(BaseModel):
    """
    Pydantic schema for User table data.

    Attributes:
    -----------
    - username: Dotaverse username.
    - password: Dotaverse user's password.
    """
    username: str
    password: str

    model_config = ConfigDict(from_attributes=True)


class PartialUserSchema(UserSchema, metaclass=_AllOptionalMeta):
    """
    Pydantic schema for User table data (PATCH). 
    """
    is_admin: Optional[bool] = None


class IndependentUserSchema(UserSchema):
    """
    Pydantic schema for User table data (subqueries).

    Attributes:
    -----------
    - id: unique identifier of the hero.
    - username: Dotaverse username.
    - password: Dotaverse user's password.
    """
    id: int
    is_admin: bool
    created_at: datetime


class UserResponse(IndependentUserSchema):
    """
    Pydantic schema for User table data.

    Attributes:
    -----------
    - id: unique identifier of the hero.
    - username: Dotaverse username.
    - password: Dotaverse user's password.
    """


class TokenSchema(BaseModel):
    """
    Pydantic schema for Token

    Attributes:
    -----------
    - access_token: generated token according to user's entry.
    - token_type: token generated type.
    """
    access_token: str
    token_type: str

    model_config = ConfigDict(from_attributes=True)
