# dependencies.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from fastapi import Depends
from database import SessionLocal

# Dependency to get DB session
async def get_db():
    async with SessionLocal() as session:
        yield session
