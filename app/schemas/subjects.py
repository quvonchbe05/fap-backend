from pydantic import BaseModel, Field
from datetime import datetime
from app.schemas.topics import TopicResponseSchema


class SubjectBaseSchema(BaseModel):
    """
    Base schema for a subject, including common fields.

    Attributes:
        title (str): The title of the subject.
        created_at (datetime): The creation timestamp of the subject.
        updated_at (datetime | None): The timestamp of the last update of the subject.
    """

    title: str = Field(...)
    created_at: datetime
    updated_at: datetime | None


class SubjectCreateEditSchema(BaseModel):
    """
    Schema for creating or editing a subject.

    Attributes:
        title (str): The title of the subject.
    """

    title: str = Field(...)


class SubjectResponseSchema(SubjectBaseSchema):
    """
    Schema for the response of a subject.

    Attributes:
        id (int): The unique identifier of the subject.
    """

    id: int


class SubjectWithTopicsResponseSchema(SubjectBaseSchema):
    """
    Schema for the response of a subject, including associated topics.

    Attributes:
        id (int): The unique identifier of the subject.
        topics (list[TopicResponseSchema]): A list of topics associated with the subject.
    """

    id: int
    topics: list[TopicResponseSchema]
