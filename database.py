from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from models import Base

DATABASE_URL = "sqlite+aiosqlite:///./database.db"  # SQLite database file

# Create Async Engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create Async Session
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Dependency to get DB session
async def get_db():
    async with async_session() as session:
        yield session  # Automatically closes session after use

# Function to initialize database
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Function to properly close database connection
async def close_db():
    await engine.dispose()