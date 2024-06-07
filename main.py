from fastapi import FastAPI
from sqladmin import Admin
from app.db.connection import engine
from app.middlewares.logs import LogsMiddleware
from fastapi.middleware.cors import CORSMiddleware

from app.routers.subjects import router as subjects_router
from app.routers.topics import router as topics_router

from app.utils.sqladmin_configs import SubjectAdmin, TopicAdmin

from config import settings

app = FastAPI(
    title="FAQ | APIs",
    version="0.1",
    debug=settings.DEBUG,
)

# Routers
app.include_router(subjects_router)
app.include_router(topics_router)

# Middlewares
app.add_middleware(LogsMiddleware, some_attribute="")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)

admin = Admin(app, engine)

# AdminPanel Pages
admin.add_view(SubjectAdmin)
admin.add_view(TopicAdmin)
