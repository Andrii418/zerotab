from pydantic import BaseModel, ConfigDict, Field

from app.schemas.person import PersonRead


class GroupCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=100)
    member_ids: list[int] = Field(default_factory=list)


class MemberAdd(BaseModel):
    person_id: int


class GroupRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    members: list[PersonRead]