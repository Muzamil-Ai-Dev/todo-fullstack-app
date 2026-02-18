"""
Chat API endpoints for the AI-powered todo chatbot.

This module provides the REST API endpoints for the chat functionality,
including the main chat endpoint and conversation management endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Optional
import traceback

from ..database.database import get_session
from ..schemas.chat import (
    ChatRequest,
    ChatResponse,
    ConversationList,
    ConversationHistory,
    ErrorResponse,
    ToolCallInfo
)
from ..services.chat_service import chat_service
from ..middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post(
    "",
    response_model=ChatResponse,
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        503: {"model": ErrorResponse}
    }
)
async def send_message(
    request: ChatRequest,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    """
    Send a chat message to the AI assistant.

    The chatbot can create, view, complete, delete, and update tasks
    through natural language conversation.

    - If conversation_id is not provided, a new conversation is created
    - If conversation_id is provided, the message is added to that conversation
    - The response includes the conversation_id for subsequent requests
    """
    try:
        user_id = current_user["user_id"]
        print(f"[Chat API] Processing message from user: {user_id}")
        print(f"[Chat API] Message: {request.message[:50]}...")

        # Validate message length
        if len(request.message) > 500:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Message must be 500 characters or less"
            )

        # Process the chat message
        result = chat_service.process_chat(
            session=session,
            user_id=user_id,
            message=request.message,
            conversation_id=request.conversation_id
        )

        print(f"[Chat API] Successfully processed chat, response length: {len(result['response'])}")

        return ChatResponse(
            conversation_id=result["conversation_id"],
            response=result["response"],
            tool_calls=[
                ToolCallInfo(
                    tool_name=tc["tool_name"],
                    arguments=tc.get("arguments") or {},
                    result=tc["result"]
                )
                for tc in result.get("tool_calls", [])
            ]
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"[Chat API] ERROR: {str(e)}")
        print(f"[Chat API] Traceback: {traceback.format_exc()}")

        if "Groq API" in str(e) or "API key" in str(e):
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="AI service temporarily unavailable. Please try again in a moment."
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )


@router.get("/conversations", response_model=ConversationList)
async def list_conversations(
    limit: int = 20,
    offset: int = 0,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    """
    Get list of conversations for the authenticated user.
    """
    user_id = current_user["user_id"]

    conversations = chat_service.get_user_conversations(
        session=session,
        user_id=user_id,
        limit=min(limit, 100),
        offset=offset
    )

    return ConversationList(conversations=conversations)


@router.get(
    "/conversations/{conversation_id}",
    response_model=ConversationHistory,
    responses={
        404: {"model": ErrorResponse}
    }
)
async def get_conversation(
    conversation_id: int,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    """
    Get a specific conversation with all messages.
    """
    user_id = current_user["user_id"]

    conversation = chat_service.get_conversation(
        session=session,
        user_id=user_id,
        conversation_id=conversation_id
    )

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conversation with ID {conversation_id} not found"
        )

    return ConversationHistory(**conversation)


@router.delete(
    "/conversations/{conversation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {"model": ErrorResponse}
    }
)
async def delete_conversation(
    conversation_id: int,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    """
    Delete a conversation and all its messages.
    """
    user_id = current_user["user_id"]

    deleted = chat_service.delete_conversation(
        session=session,
        user_id=user_id,
        conversation_id=conversation_id
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conversation with ID {conversation_id} not found"
        )

    return None
