from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text 
from sqlalchemy.exc import SQLAlchemyError 
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper


router = APIRouter(prefix="/health", tags=["Health"])

@router.get("/live")
async def liveness():
    return {"status": "ok"}


@router.get("/ready")
async def readiness(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    try:
        await session.execute(text("SELECT 1"))
    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=503,
            detail="Database is unavailable",
        ) from exc

    return {
        "status": "ok",
        "database": "available",
    }