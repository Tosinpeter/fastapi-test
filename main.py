from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import Base, engine
from dependencies import get_db
from models import User

app = FastAPI()

# Pydantic models for user input and output
class UserInCreate(BaseModel):
    name: str
    email: str

class UserOut(BaseModel):
    id: int
    name: str
    email: str

# Async schema creation
async def create_tables():
    async with engine.begin() as conn:
        # This will create tables
        await conn.run_sync(Base.metadata.create_all)

# Call this function before starting the app or when the app is first launched
# FastAPI startup event
@app.on_event("startup")
async def on_startup():
    # Create tables during startup
    await create_tables()

# Create a new user
@app.post("/users/", response_model=UserOut)
async def create_user(user: UserInCreate, db: AsyncSession = Depends(get_db)):
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

# Get all users
@app.get("/users/", response_model=list[UserOut])
async def get_users(db: AsyncSession = Depends(get_db)):
    query = select(User)
    result = await db.execute(query)
    users = result.scalars().all()
    return users

# Get a single user by ID
@app.get("/users/{user_id}", response_model=UserOut)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    query = select(User).filter(User.id == user_id)
    result = await db.execute(query)
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user