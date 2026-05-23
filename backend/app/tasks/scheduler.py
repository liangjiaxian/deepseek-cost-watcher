import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR, JobExecutionEvent
from sqlalchemy import select

from app.services.balance_service import poll_balance
from app.services.cost_service import poll_usage_cost

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()
_job_id = "poll_balance"
_cost_job_id = "poll_usage_cost"


def _job_listener(event: JobExecutionEvent):
    if event.exception:
        logger.error("Scheduler job '%s' failed: %s", event.job_id, event.exception)
    else:
        logger.info("Scheduler job '%s' completed (retval=%s)", event.job_id, event.retval)


async def start_scheduler():
    scheduler.add_listener(_job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    interval = await _load_interval()
    _ensure_job(interval)


def _ensure_job(interval_minutes: int):
    scheduler.add_job(
        poll_balance,
        "interval",
        minutes=interval_minutes,
        id=_job_id,
        replace_existing=True,
    )
    scheduler.add_job(
        poll_usage_cost,
        "interval",
        minutes=max(interval_minutes, 60),
        id=_cost_job_id,
        replace_existing=True,
    )
    if not scheduler.running:
        scheduler.start()
    logger.info("Polling jobs scheduled (balance=%dmin, cost=%dmin)", interval_minutes, max(interval_minutes, 60))


async def reschedule_polling(interval_minutes: int):
    _ensure_job(interval_minutes)


async def _load_interval() -> int:
    from app.core.database import async_session_factory
    from app.models.system_config import SystemConfig
    try:
        async with async_session_factory() as db:
            stmt = select(SystemConfig).where(SystemConfig.config_key == "poll_interval")
            row = (await db.execute(stmt)).scalar_one_or_none()
            if row:
                return int(row.config_value)
    except Exception:
        pass
    return 30
