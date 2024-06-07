from pydantic import BaseModel, Field
from datetime import datetime


class TopicBaseSchema(BaseModel):
    """
    Base schema for a topic, including common fields.

    Attributes:
        title (str): The title of the topic.
        description (str): A brief description of the topic.
        created_at (datetime): The timestamp when the topic was created.
        updated_at (datetime | None): The timestamp of the last update to the topic, or None if never updated.
    """

    title: str = Field(...)
    description: str = Field(...)
    created_at: datetime
    updated_at: datetime | None


class TopicCreateEditSchema(BaseModel):
    """
    Schema for creating or editing a topic.

    Attributes:
        title (str): The title of the topic.
        description (str): A brief description of the topic.
        subject_id (int): The ID of the subject to which the topic belongs.
    """

    title: str = Field(...)
    description: str = Field(...)
    subject_id: int = Field(ge=1)


class TopicResponseSchema(TopicBaseSchema):
    """
    Schema for the response of a topic.

    Attributes:
        id (int): The unique identifier of the topic.
    """

    id: int
