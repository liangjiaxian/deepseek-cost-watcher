from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from .config import settings


engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {},
)

async_session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    import app.models
    async with engine.begin() as conn:
        if "sqlite" in settings.database_url:
            await conn.exec_driver_sql("PRAGMA journal_mode=WAL;")
            await conn.exec_driver_sql("PRAGMA foreign_keys=ON;")
        await conn.run_sync(Base.metadata.create_all)
        await conn.run_sync(add_missing_columns)


def add_missing_columns(sync_conn):
    """Add columns introduced after the first release to existing tables.

    create_all() only creates missing tables, so a database created before a
    field existed would otherwise lack it. Only nullable columns are added
    here; adding a NOT NULL column without a server default would fail.
    """
    from sqlalchemy import inspect

    inspector = inspect(sync_conn)
    for table in Base.metadata.sorted_tables:
        if not inspector.has_table(table.name):
            continue
        existing = {col["name"] for col in inspector.get_columns(table.name)}
        for column in table.columns:
            if column.name in existing or not column.nullable:
                continue
            col_type = column.type.compile(sync_conn.dialect)
            sync_conn.exec_driver_sql(
                f"ALTER TABLE {table.name} ADD COLUMN {column.name} {col_type}"
            )
