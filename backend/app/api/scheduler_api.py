from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from app.core.database import get_db
from app.schemas.common import ApiResponse
from app.models.scheduler_log import SchedulerLog
from app.services.balance_service import poll_balance
from app.services.cost_service import poll_usage_cost

router = APIRouter(prefix="/api/v1/scheduler", tags=["Scheduler"])


@router.get("/logs")
async def get_scheduler_logs(limit: int = Query(default=10, le=50), db: AsyncSession = Depends(get_db)):
    stmt = select(SchedulerLog).order_by(desc(SchedulerLog.id)).limit(limit)
    rows = (await db.execute(stmt)).scalars().all()
    data = []
    for r in rows:
        data.append({
            "id": r.id,
            "task_name": r.task_name,
            "status": r.status,
            "message": r.message,
            "started_at": r.started_at.isoformat() + "Z" if r.started_at else None,
            "finished_at": r.finished_at.isoformat() + "Z" if r.finished_at else None,
        })
    return ApiResponse(data=data)


@router.post("/trigger")
async def trigger_scheduler():
    await poll_balance()
    return ApiResponse(message="Scheduler triggered")


@router.post("/trigger-cost")
async def trigger_cost():
    await poll_usage_cost()
    return ApiResponse(message="Cost poll triggered")
