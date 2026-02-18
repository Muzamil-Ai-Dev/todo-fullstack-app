from sqlmodel import create_engine, Session
from sqlalchemy import text
from sqlalchemy.pool import NullPool
from ..config.settings import settings
from typing import Generator

# Create the database engine with connection pooling for Neon PostgreSQL
# Neon requires specific pool settings to handle serverless connections
engine = create_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_pre_ping=True,  # Verify connections before using them
    pool_recycle=300,  # Recycle connections after 5 minutes
    pool_size=5,  # Maximum number of connections to keep open
    max_overflow=10,  # Maximum overflow connections
    connect_args={
        "connect_timeout": 10,
        "keepalives": 1,
        "keepalives_idle": 30,
        "keepalives_interval": 10,
        "keepalives_count": 5,
    }
)

def get_session() -> Generator[Session, None, None]:
    """
    Get a database session
    """
    with Session(engine) as session:
        yield session

def init_db() -> None:
    """
    Initialize the database by creating all tables
    """
    from sqlmodel import SQLModel
    from ..models.user import User  # noqa: F401
    from ..models.task import Task  # noqa: F401
    from ..models.conversation import Conversation, Message  # noqa: F401

    # Create all tables defined in SQLModel models
    SQLModel.metadata.create_all(engine)

    # Verify connection
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))