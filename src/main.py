import logging

from fastapi import APIRouter, FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.auth.router import auth_router
from src.companies.routers import companies_router
from src.config import get_app_settings
from src.core.middlewares import ProcessTimeMiddleware
from src.groups.routers import groups_router
from src.roles.routers import roles_router
from src.settings.routers import settings_router
from src.timezones.routers import timezones_router
from src.users.router import users_router

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

settings = get_app_settings()

app = FastAPI(title="Backend service")
v1_api_router = APIRouter()

v1_api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
v1_api_router.include_router(users_router, prefix="/users", tags=["Users"])
v1_api_router.include_router(companies_router, prefix="/companies", tags=["Companies"])
v1_api_router.include_router(groups_router, prefix="/groups", tags=["Groups"])
v1_api_router.include_router(roles_router, prefix="/roles", tags=["Roles"])
v1_api_router.include_router(timezones_router, prefix="/timezones", tags=["Timezones"])
v1_api_router.include_router(settings_router, prefix="/settings", tags=["Settings"])
app.include_router(v1_api_router, prefix="/v1")

app.add_middleware(ProcessTimeMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
