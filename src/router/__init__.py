from fastapi import APIRouter

from . import pipeline_api


api_router = APIRouter()
api_router.include_router(pipeline_api.router,
                          prefix="/api",)