import json
from sqlalchemy import create_engine, Column, String, Float, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

# Database configuration
DATABASE_URL = "postgresql+asyncpg://user:password@localhost/dbname"  # Update with your actual DB URL
Base = declarative_base()

# PredictionResults model
class PredictionResults(Base):
    __tablename__ = 'prediction_results'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String, nullable=False)
    classification = Column(String, nullable=False)
    probabilities = Column(String, nullable=False)  # Store as JSON string

# Create an asynchronous database engine
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    """Create the database tables asynchronously."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def insert_prediction_result(filename: str, classification: str, probabilities: list):
    """Insert a new prediction result into the database asynchronously."""
    async with AsyncSessionLocal() as session:
        async with session.begin():
            new_result = PredictionResults(
                filename=filename,
                classification=classification,
                probabilities=json.dumps(probabilities)  # Store as JSON string
            )
            session.add(new_result)
            await session.commit()

async def get_db():
    """Dependency to provide the database session asynchronously."""
    async with AsyncSessionLocal() as session:
        yield session  # Provide the session for the request
