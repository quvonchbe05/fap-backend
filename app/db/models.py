from app.db.connection import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Text,
)
from sqlalchemy.orm import relationship
from datetime import datetime


class BaseModel:
    """
    Base model class for common attributes.

    Attributes:
        id (int): The primary key identifier.
        created_at (datetime): The timestamp when the record was created.
        updated_at (datetime | None): The timestamp of the last update to the record, or None if never updated.
    """

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, onupdate=datetime.now(), nullable=True)


class SubjectModel(Base, BaseModel):
    """
    ORM model for the subjects table.

    Attributes:
        title (str): The title of the subject.
        topics (relationship): The relationship to associated topics.
    """

    __tablename__ = "subjects"

    title: str = Column(String(255), nullable=False)

    topics = relationship(
        "TopicModel", cascade="all, delete-orphan", back_populates="subject"
    )

    def __repr__(self):
        return f"Subject: {self.title}"


class TopicModel(Base, BaseModel):
    """
    ORM model for the topics table.

    Attributes:
        title (str): The title of the topic.
        description (str): A brief description of the topic.
        subject_id (int): The ID of the subject to which the topic belongs.
        subject (relationship): The relationship to the associated subject.
    """

    __tablename__ = "topics"

    title: str = Column(String(255), nullable=False)
    description: str = Column(Text, nullable=False)

    subject_id: int = Column(
        Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False
    )
    subject = relationship("SubjectModel", back_populates="topics")

    def __repr__(self):
        return f"Topic: {self.title}"
