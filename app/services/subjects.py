from fastapi import HTTPException
from app.db.connection import AsyncSession
from app.db.models import SubjectModel
from app.schemas.subjects import SubjectCreateEditSchema
from sqlalchemy import select, insert, update, delete, desc
from sqlalchemy.orm import selectinload


async def get_list_service(session: AsyncSession):
    """
    Retrieve a list of subjects, ordered by descending ID.

    Args:
        session (AsyncSession): The database session.

    Returns:
        List[SubjectModel]: A list of subjects.
    """
    query = select(SubjectModel).order_by(desc(SubjectModel.id))
    result = await session.execute(query)
    return result.scalars().all()


async def get_one_service(subject_id: int, session: AsyncSession):
    """
    Retrieve a specific subject by its ID, including its associated topics.

    Args:
        subject_id (int): The ID of the subject to retrieve.
        session (AsyncSession): The database session.

    Raises:
        HTTPException: If the subject is not found.

    Returns:
        SubjectModel: The subject with its topics.
    """
    query = select(SubjectModel).where(SubjectModel.id == subject_id)
    exist = await session.execute(query)
    if not exist.scalar():
        raise HTTPException(status_code=404, detail="Subject not found!")

    query = (
        select(SubjectModel)
        .options(selectinload(SubjectModel.topics))
        .where(SubjectModel.id == subject_id)
    )
    result = await session.execute(query)
    return result.scalar()


async def create_service(subject: SubjectCreateEditSchema, session: AsyncSession):
    """
    Create a new subject if it does not already exist.

    Args:
        subject (SubjectCreateEditSchema): The subject data for creation.
        session (AsyncSession): The database session.

    Raises:
        HTTPException: If a subject with the same title already exists.

    Returns:
        SubjectModel: The created subject.
    """
    query = select(SubjectModel).where(SubjectModel.title == subject.title)
    exist = await session.execute(query)
    if exist.scalar() is not None:
        raise HTTPException(status_code=400, detail="Subject already exists")

    stmt = insert(SubjectModel).values(**subject.model_dump()).returning(SubjectModel)
    result = await session.execute(stmt)
    await session.commit()
    created = result.scalar()

    return created


async def edit_service(
    subject_id: int, subject: SubjectCreateEditSchema, session: AsyncSession
):
    """
    Edit an existing subject by its ID.

    Args:
        subject_id (int): The ID of the subject to edit.
        subject (SubjectCreateEditSchema): The subject data for updating.
        session (AsyncSession): The database session.

    Raises:
        HTTPException: If the subject is not found.

    Returns:
        SubjectModel: The updated subject.
    """
    query = select(SubjectModel).where(SubjectModel.id == subject_id)
    exist = await session.execute(query)
    if not exist.scalar():
        raise HTTPException(status_code=404, detail="Subject not found!")

    stmt = (
        update(SubjectModel)
        .values(**subject.model_dump())
        .where(SubjectModel.id == subject_id)
        .returning(SubjectModel)
    )
    result = await session.execute(stmt)
    await session.commit()
    updated = result.scalar()

    return updated


async def delete_service(subject_id: int, session: AsyncSession):
    """
    Delete a subject by its ID.

    Args:
        subject_id (int): The ID of the subject to delete.
        session (AsyncSession): The database session.

    Raises:
        HTTPException: If the subject is not found.

    Returns:
        str: Success message indicating deletion.
    """
    query = select(SubjectModel).where(SubjectModel.id == subject_id)
    exist = await session.execute(query)
    if not exist.scalar():
        raise HTTPException(status_code=404, detail="Subject not found!")

    stmt = delete(SubjectModel).where(SubjectModel.id == subject_id)
    await session.execute(stmt)
    await session.commit()
    return "success"
