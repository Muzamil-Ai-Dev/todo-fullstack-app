"""
Chat schemas for request/response validation in the AI-powered todo chatbot.

These schemas define the API contracts for the chat endpoint.
"""

from pydantic import BaseModel, Field
from typing import Optional, List


class ChatRequest(BaseModel):
    """Request schema for sending a chat message"""
    conversation_id: Optional[int] = Field(
        default=None,
        description="Existing conversation ID. If not provided, a new conversation is created."
    )
    message: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="User's natural language message"
    )


class ToolCallInfo(BaseModel):
    """Information about an MCP tool invoked during processing"""
    tool_name: str = Field(description="Name of the MCP tool invoked")
    arguments: Optional[dict] = Field(default={}, description="Arguments passed to the tool")
    result: dict = Field(description="Result returned by the tool")


class ChatResponse(BaseModel):
    """Response schema for the chat endpoint"""
    conversation_id: int = Field(description="The conversation ID (new or existing)")
    response: str = Field(description="AI assistant's response text")
    tool_calls: List[ToolCallInfo] = Field(
        default=[],
        description="List of MCP tools invoked during processing"
    )


class MessageRead(BaseModel):
    """Schema for reading a single message"""
    id: int
    role: str
    content: str
    created_at: str


class ConversationHistory(BaseModel):
    """Schema for conversation with message history"""
    conversation_id: int
    messages: List[MessageRead]
    created_at: str
    updated_at: str


class ConversationListItem(BaseModel):
    """Schema for a conversation in the list"""
    id: int
    created_at: str
    updated_at: str
    message_count: int


class ConversationList(BaseModel):
    """Schema for list of conversations"""
    conversations: List[ConversationListItem]


class ErrorResponse(BaseModel):
    """Schema for error responses"""
    error: str
    detail: Optional[str] = None
