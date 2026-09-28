from datetime import datetime

from pydantic import BaseModel, Field


class GroupCreateSchema(BaseModel):
    group_name: str = Field(min_length=1, max_length=100)


class GroupUpdateSchema(BaseModel):
    group_name: str = Field(min_length=1, max_length=100)


class GroupOutputSchema(BaseModel):
    id: int
    group_name: str
    owner: int
    created_date: datetime

    class Config:
        from_attributes = True


class GroupPeopleCreateSchema(BaseModel):
    group_id: int = Field(gt=0)
    user: int = Field(gt=0)


class GroupPeopleOutputSchema(BaseModel):
    id: int
    group_id: int
    user: int
    created_date: datetime

    class Config:
        from_attributes = True


class GroupMessageCreateSchema(BaseModel):
    group_id: int = Field(gt=0)
    message: str = Field(min_length=1)


class GroupMessageUpdateSchema(BaseModel):
    message: str = Field(min_length=1)


class GroupMessageOutputSchema(BaseModel):
    id: int
    group_id: int
    user: int
    message: str
    created_date: datetime

    class Config:
        from_attributes = True

# schema