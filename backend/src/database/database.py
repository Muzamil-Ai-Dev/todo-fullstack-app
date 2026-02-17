from sqlmodel import create_engine, Session
from sqlalchemy import text
from ..config.settings import settings
from typing import Generator

# Create the database engine
engine = create_engine(settings.DATABASE_URL, echo=False)

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