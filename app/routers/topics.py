from fastapi import APIRouter, Depends
from app.db.connection import AsyncSession, get_async_session
from app.schemas.topics import (
    TopicCreateEditSchema,
    TopicResponseSchema,
)
from app.services.topics import (
    get_list_service,
    get_one_service,
    get_by_subject_service,
    create_service,
    edit_service,
    delete_service,
)

router = APIRouter(tags=["Topics"], prefix="/api/topics")


@router.get("", response_model=list[TopicResponseSchema])
async def get_list(session: AsyncSession = Depends(get_async_session)):
    """
    Retrieve a list of topics.

    Args:
        session (AsyncSession): The database session dependency.

    Returns:
        List[TopicResponseSchema]: A list of topics.
    """
    return await get_list_service(session)


@router.get("/{topic_id}", response_model=TopicResponseSchema)
async def get_one(topic_id: int, session: AsyncSession = Depends(get_async_session)):
    """
    Retrieve a specific topic by its ID.

    Args:
        topic_id (int): The ID of the topic to retrieve.
        session (AsyncSession): The database session dependency.

    Returns:
        TopicResponseSchema: The retrieved topic.
    """
    return await get_one_service(topic_id, session)


@router.get("/subject/{subject_id}", response_model=list[TopicResponseSchema])
async def get_by_subject(
    subject_id: int, session: AsyncSession = Depends(get_async_session)
):
    """
    Retrieve a list of topics associated with a specific subject ID.

    Args:
        subject_id (int): The ID of the subject.
        session (AsyncSession): The database session dependency.

    Returns:
        List[TopicResponseSchema]: A list of topics associated with the subject.
    """
    return await get_by_subject_service(subject_id, session)


@router.post("/create", response_model=TopicResponseSchema)
async def create(
    topic: TopicCreateEditSchema, session: AsyncSession = Depends(get_async_session)
):
    """
    Create a new topic.

    Args:
        topic (TopicCreateEditSchema): The topic data for creation.
        session (AsyncSession): The database session dependency.

    Returns:
        TopicResponseSchema: The created topic.
    """
    return await create_service(topic, session)


@router.put("/edit/{topic_id}", response_model=TopicResponseSchema)
async def edit(
    topic_id: int,
    topic: TopicCreateEditSchema,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Edit an existing topic by its ID.

    Args:
        topic_id (int): The ID of the topic to edit.
        topic (TopicCreateEditSchema): The topic data for updating.
        session (AsyncSession): The database session dependency.

    Returns:
        TopicResponseSchema: The updated topic.
    """
    return await edit_service(topic_id, topic, session)


@router.delete("/delete/{topic_id}")
async def delete(topic_id: int, session: AsyncSession = Depends(get_async_session)):
    """
    Delete a topic by its ID.

    Args:
        topic_id (int): The ID of the topic to delete.
        session (AsyncSession): The database session dependency.

    Returns:
        str: Success message indicating deletion.
    """
    return await delete_service(topic_id, session)
