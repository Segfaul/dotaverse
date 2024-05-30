from datetime import datetime

from pydantic import BaseModel, ConfigDict


class LogSchema(BaseModel):
    """
    Pydantic schema for Token

    Attributes:
    -----------
    - created_at: date logs were written.
    - level: log priority level.
    - message: log record description.
    """
    created_at: datetime
    level: str
    service: str
    message: str

    model_config = ConfigDict(from_attributes=True)
