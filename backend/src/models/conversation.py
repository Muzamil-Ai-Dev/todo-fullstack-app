"""
Conversation and Message models for the AI-powered todo chatbot.

These models support the stateless chat architecture where conversation
history is persisted to the database for context continuity.
"""

from sqlmodel import SQLModel, Field, Relationship, Index
from typing import Optional, List
from datetime import datetime


class Conversation(SQLModel, table=True):
    """
    Conversation model representing a chat session between a user and the AI assistant.

    A user can have multiple conversations over time. Each conversation
    maintains a history of messages for context-aware responses.
    """
    __tablename__ = "conversation"
    __table_args__ = (
        Index("idx_conversation_user", "user_id"),
        Index("idx_conversation_updated", "updated_at"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id", nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationships
    user: "User" = Relationship(back_populates="conversations")
    messages: List["Message"] = Relationship(back_populates="conversation")


class Message(SQLModel, table=True):
    """
    Message model representing individual messages within a conversation.

    Messages are ordered chronologically within a conversation and can
    have role 'user' or 'assistant'.
    """
    __tablename__ = "message"
    __table_args__ = (
        Index("idx_message_conversation", "conversation_id"),
        Index("idx_message_created", "created_at"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversation.id", nullable=False)
    user_id: str = Field(foreign_key="user.id", nullable=False)
    role: str = Field(nullable=False)  # 'user' or 'assistant'
    content: str = Field(nullable=False, max_length=500)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationships
    conversation: "Conversation" = Relationship(back_populates="messages")
    user: "User" = Relationship(back_populates="messages")


# Schema classes for API responses

class MessageRead(SQLModel):
    """Schema for reading message data"""
    id: int
    role: str
    content: str
    created_at: datetime


class ConversationRead(SQLModel):
    """Schema for reading conversation data"""
    id: int
    user_id: str
    created_at: datetime
    updated_at: datetime


class ConversationHistory(SQLModel):
    """Schema for conversation with messages"""
    conversation_id: int
    messages: List[MessageRead]
    created_at: datetime
    updated_at: datetime


class ConversationListItem(SQLModel):
    """Schema for conversation list item"""
    id: int
    created_at: datetime
    updated_at: datetime
    message_count: int
