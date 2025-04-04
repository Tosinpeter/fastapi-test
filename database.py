# database.py
from databases import Database
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL (using asyncpg with SQLAlchemy)
DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost/postgres"

# Create an Async engine (for SQLAlchemy)
engine = create_async_engine(DATABASE_URL, echo=True)

# Create a SessionLocal to manage database sessions
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# SQLAlchemy's base class to create models
metadata = MetaData()
Base = declarative_base(metadata=metadata)

# Databases connection for asyncpg
database = Database(DATABASE_URL)
