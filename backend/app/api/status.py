from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from app.core.database import get_db
from app.schemas.common import ApiResponse
from app.services.key_service import KeyService
from app.services.proxy_service import ProxyService
from app.tasks.scheduler import scheduler, _job_id
from app.models.scheduler_log import SchedulerLog

router = APIRouter(tags=["Status"])


@router.get("/api/v1/status")
async def get_status(db: AsyncSession = Depends(get_db)):
    key_service = KeyService(db)
    api_key = await key_service.get_first_active_key()

    base = {
        "status": "ok",
        "keys_configured": len(await key_service.list_keys()),
    }

    if api_key:
        proxy = ProxyService()
        ok, msg, balance = await proxy.test_connection(api_key)
        base["deepseek_connected"] = ok
        base["balance"] = balance
        if not ok:
            base["status"] = "error"
    else:
        base["deepseek_connected"] = False
        base["balance"] = None
        base["status"] = "no_key"

    job = scheduler.get_job(_job_id)
    if job:
        base["scheduler"] = {
            "interval_minutes": job.trigger.interval_length // 60 if hasattr(job.trigger, "interval_length") else None,
            "next_run_time": job.next_run_time.isoformat() if job.next_run_time else None,
        }
    else:
        base["scheduler"] = None

    stmt = select(SchedulerLog).order_by(desc(SchedulerLog.id)).limit(1)
    last = (await db.execute(stmt)).scalar_one_or_none()
    if last:
        base["scheduler_last_run"] = last.started_at.isoformat() + "Z" if last.started_at else None
        base["scheduler_last_status"] = last.status
        base["scheduler_last_message"] = last.message

    return ApiResponse(data=base)
