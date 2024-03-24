from datetime import datetime

from pydantic import BaseModel, ConfigDict

from backend.api.util import _AllOptionalMeta


class RequestSchema(BaseModel):
    """
    Pydantic schema for the data in the Request table.

    Attributes:
    - opendota_link: link associated with the request.
    - status: status of the request.
    """
    opendota_link: str
    status: int

    model_config = ConfigDict(from_attributes=True)


class PartialRequestSchema(RequestSchema, metaclass=_AllOptionalMeta):
    """
    Pydantic schema for the data in the Request table (PATCH). 
    """


class IndependentRequestSchema(RequestSchema):
    """
    Pydantic schema for the data in the Request table (subqueries).

    Attributes:
    - id: unique identifier of the request.
    - opendota_link: link associated with the request.
    - status: status of the request.
    - created_at: date the request was created.
    """
    id: int
    created_at: datetime


class RequestResponse(IndependentRequestSchema):
    """
    Pydantic schema for the data in the Request table.

    Attributes:
    - id: unique identifier of the request.
    - opendota_link: link associated with the request.
    - status: status of the request.
    - created_at: date the request was created.
    """
