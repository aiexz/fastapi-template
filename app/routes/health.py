from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from starlette.responses import Response

from app.database import Database
from app.dependancies import DatabaseDependency
import app

router = APIRouter()


class Health(BaseModel):
    alive: bool
    version: str


@router.get("/health",
            response_model=Health,
            status_code=200,
            responses={200: {"model": Health}},
            summary="Health check",
            description="Check if the service is alive",
            tags=["Health"]
            )
async def health(
        database: Annotated[Database, Depends(DatabaseDependency)],
        response: Response
):
    ping = await database.ping()
    if ping:
        response.status_code = 200
    else:
        response.status_code = 500
    return Health(alive=ping, version=app.__version__)
# TODO: add git version

