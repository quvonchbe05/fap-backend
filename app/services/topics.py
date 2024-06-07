from fastapi import HTTPException
from app.db.connection import AsyncSession
from app.db.models import TopicModel, SubjectModel
from app.schemas.topics import TopicCreateEditSchema
from sqlalchemy import select, insert, update, delete, desc


async def get_list_service(session: AsyncSession):
    """
    Retrieve a list of topics, ordered by descending ID.

    Args:
        session (AsyncSession): The database session.

    Returns:
        List[TopicModel]: A list of topics.
    """
    query = select(TopicModel).order_by(desc(TopicModel.id))
    result = await session.execute(query)
    return result.scalars().all()


async def get_one_service(topic_id: int, session: AsyncSession):
    """
    Retrieve a specific topic by its ID.

    Args:
        topic_id (int): The ID of the topic to retrieve.
        session (AsyncSession): The database session.

    Raises:
        HTTPException: If the topic is not found.

    Returns:
        TopicModel: The retrieved topic.
    """
    query = select(TopicModel).where(TopicModel.id == topic_id)
    exist = await session.execute(query)
    if not exist.scalar():
        raise HTTPException(status_code=404, detail="Topic not found!")

    query = select(TopicModel).where(TopicModel.id == topic_id)
    result = await session.execute(query)
    return result.scalar()


async def get_by_subject_service(subject_id: int, session: AsyncSession):
    """
    Retrieve a list of topics associated with a specific subject ID.

    Args:
        subject_id (int): The ID of the subject.
        session (AsyncSession): The database session.

    Raises:
        HTTPException: If the subject is not found.

    Returns:
        List[TopicModel]: A list of topics associated with the subject.
    """
    query = select(SubjectModel).where(SubjectModel.id == subject_id)
    exist = await session.execute(query)
    if not exist.scalar():
        raise HTTPException(status_code=404, detail="Subject not found!")

    query = select(TopicModel).where(TopicModel.subject_id == subject_id)
    result = await session.execute(query)
    return result.scalars().all()


async def create_service(topic: TopicCreateEditSchema, session: AsyncSession):
    """
    Create a new topic if it does not already exist.

    Args:
        topic (TopicCreateEditSchema): The topic data for creation.
        session (AsyncSession): The database session.

    Raises:
        HTTPException: If a topic with the same title already exists.

    Returns:
        TopicModel: The created topic.
    """
    query = select(TopicModel).where(TopicModel.title == topic.title)
    exist = await session.execute(query)
    if exist.scalar() is not None:
        raise HTTPException(status_code=400, detail="Topic already exists")

    stmt = insert(TopicModel).values(**topic.model_dump()).returning(TopicModel)
    result = await session.execute(stmt)
    await session.commit()
    created = result.scalar()

    return created


async def edit_service(
    topic_id: int, topic: TopicCreateEditSchema, session: AsyncSession
):
    """
    Edit an existing topic by its ID.

    Args:
        topic_id (int): The ID of the topic to edit.
        topic (TopicCreateEditSchema): The topic data for updating.
        session (AsyncSession): The database session.

    Raises:
        HTTPException: If the topic is not found.

    Returns:
        TopicModel: The updated topic.
    """
    query = select(TopicModel).where(TopicModel.id == topic_id)
    exist = await session.execute(query)
    if not exist.scalar():
        raise HTTPException(status_code=404, detail="Topic not found!")

    stmt = (
        update(TopicModel)
        .values(**topic.model_dump())
        .where(TopicModel.id == topic_id)
        .returning(TopicModel)
    )
    result = await session.execute(stmt)
    await session.commit()
    updated = result.scalar()

    return updated


async def delete_service(topic_id: int, session: AsyncSession):
    """
    Delete a topic by its ID.

    Args:
        topic_id (int): The ID of the topic to delete.
        session (AsyncSession): The database session.

    Raises:
        HTTPException: If the topic is not found.

    Returns:
        str: Success message indicating deletion.
    """
    query = select(TopicModel).where(TopicModel.id == topic_id)
    exist = await session.execute(query)
    if not exist.scalar():
        raise HTTPException(status_code=404, detail="Topic not found!")

    stmt = delete(TopicModel).where(TopicModel.id == topic_id)
    await session.execute(stmt)
    await session.commit()
    return "success"
