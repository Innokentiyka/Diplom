from datetime import datetime, timedelta

from beanie import PydanticObjectId
from pydantic import BaseModel, alias_generators, ConfigDict, Field


class SecretDTO(BaseModel):
    model_config = ConfigDict(alias_generator=alias_generators.to_camel, populate_by_name=True,
                              arbitrary_types_allowed=True)

    id: PydanticObjectId | None = Field(serialization_alias='_id', default=None)
    code_phrase: str | None = ''
    secret: str | bytes
    secret_key: str | None = None
    is_active: bool | None = True
    lifetime_days: int | None = 7
    expire_at: datetime | None = datetime.utcnow() + timedelta(days=7)
