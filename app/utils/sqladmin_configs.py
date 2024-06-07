from sqladmin import ModelView
from app.db.models import SubjectModel, TopicModel


class SubjectAdmin(ModelView, model=SubjectModel):
    """
    Admin view for the SubjectModel.

    This class provides an admin interface for managing subjects in the database.

    Attributes:
        column_list (list): List of columns to display in the admin interface.
    """

    column_list = [
        SubjectModel.id,
        SubjectModel.title,
        SubjectModel.created_at,
        SubjectModel.updated_at,
    ]


class TopicAdmin(ModelView, model=TopicModel):
    """
    Admin view for the TopicModel.

    This class provides an admin interface for managing topics in the database.

    Attributes:
        column_list (list): List of columns to display in the admin interface.
    """

    column_list = [
        TopicModel.id,
        TopicModel.title,
        TopicModel.created_at,
        TopicModel.updated_at,
    ]
