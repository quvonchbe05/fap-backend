from fastapi import APIRouter, Depends
from app.db.connection import AsyncSession, get_async_session
from app.schemas.subjects import (
    SubjectCreateEditSchema,
    SubjectResponseSchema,
    SubjectWithTopicsResponseSchema,
)
from app.services.subjects import (
    get_list_service,
    get_one_service,
    create_service,
    edit_service,
    delete_service,
)

router = APIRouter(tags=["Subjects"], prefix="/api/subjects")


@router.get("", response_model=list[SubjectResponseSchema])
async def get_list(session: AsyncSession = Depends(get_async_session)):
    """
    Retrieve a list of subjects.

    Args:
        session (AsyncSession): The database session dependency.

    Returns:
        List[SubjectResponseSchema]: A list of subjects.
    """
    return await get_list_service(session)


@router.get("/{subject_id}", response_model=SubjectWithTopicsResponseSchema)
async def get_one(subject_id: int, session: AsyncSession = Depends(get_async_session)):
    """
    Retrieve a specific subject by its ID.

    Args:
        subject_id (int): The ID of the subject to retrieve.
        session (AsyncSession): The database session dependency.

    Returns:
        SubjectWithTopicsResponseSchema: The subject with its associated topics.
    """
    return await get_one_service(subject_id, session)


@router.post("/create", response_model=SubjectResponseSchema)
async def create(
    subject: SubjectCreateEditSchema, session: AsyncSession = Depends(get_async_session)
):
    """
    Create a new subject.

    Args:
        subject (SubjectCreateEditSchema): The subject data for creation.
        session (AsyncSession): The database session dependency.

    Returns:
        SubjectResponseSchema: The created subject.
    """
    return await create_service(subject, session)


@router.put("/edit/{subject_id}", response_model=SubjectResponseSchema)
async def edit(
    subject_id: int,
    subject: SubjectCreateEditSchema,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Edit an existing subject by its ID.

    Args:
        subject_id (int): The ID of the subject to edit.
        subject (SubjectCreateEditSchema): The subject data for updating.
        session (AsyncSession): The database session dependency.

    Returns:
        SubjectResponseSchema: The updated subject.
    """
    return await edit_service(subject_id, subject, session)


@router.delete("/delete/{subject_id}")
async def delete(subject_id: int, session: AsyncSession = Depends(get_async_session)):
    """
    Delete a subject by its ID.

    Args:
        subject_id (int): The ID of the subject to delete.
        session (AsyncSession): The database session dependency.

    Returns:
        None
    """
    return await delete_service(subject_id, session)
