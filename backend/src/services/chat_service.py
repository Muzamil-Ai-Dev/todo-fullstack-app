"""
Chat Service for the AI-powered todo chatbot.

This service handles the core chat logic including:
- Groq API integration for LLM responses
- Conversation management
- Message persistence
- MCP tool orchestration
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from sqlmodel import Session, select
from groq import Groq
import os

from ..config.settings import settings
from ..models.conversation import Conversation, Message
from ..mcp.server import get_tool_definitions
from ..mcp.tools import execute_tool


class ChatService:
    """
    Service for handling chat interactions with the AI assistant.

    Uses Groq API for LLM responses and MCP tools for task operations.
    """

    def __init__(self):
        """Initialize the chat service with Groq client."""
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = "llama-3.3-70b-versatile"  # Free tier model

    def get_or_create_conversation(
        self,
        session: Session,
        user_id: str,
        conversation_id: Optional[int] = None
    ) -> Conversation:
        """
        Get an existing conversation or create a new one.

        Args:
            session: Database session
            user_id: ID of the user
            conversation_id: Optional existing conversation ID

        Returns:
            Conversation object
        """
        if conversation_id:
            try:
                stmt = select(Conversation).where(
                    Conversation.id == conversation_id,
                    Conversation.user_id == user_id
                )
                conversation = session.exec(stmt).first()
                if conversation:
                    print(f"[ChatService] Found existing conversation: {conversation_id}")
                    return conversation
                else:
                    print(f"[ChatService] Conversation {conversation_id} not found, creating new one")
            except Exception as e:
                print(f"[ChatService] Error finding conversation: {e}")

        # Create new conversation
        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        print(f"[ChatService] Created new conversation: {conversation.id}")
        return conversation

    def get_conversation_history(
        self,
        session: Session,
        conversation_id: int
    ) -> List[Dict[str, str]]:
        """
        Get message history for a conversation.

        Args:
            session: Database session
            conversation_id: ID of the conversation

        Returns:
            List of message dictionaries with role and content
        """
        stmt = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at)
        messages = session.exec(stmt).all()

        return [{"role": m.role, "content": m.content} for m in messages]

    def save_message(
        self,
        session: Session,
        conversation_id: int,
        user_id: str,
        role: str,
        content: str
    ) -> Message:
        """
        Save a message to the conversation.

        Args:
            session: Database session
            conversation_id: ID of the conversation
            user_id: ID of the user
            role: 'user' or 'assistant'
            content: Message content

        Returns:
            Saved Message object
        """
        message = Message(
            conversation_id=conversation_id,
            user_id=user_id,
            role=role,
            content=content
        )
        session.add(message)

        # Update conversation's updated_at timestamp
        stmt = select(Conversation).where(Conversation.id == conversation_id)
        conversation = session.exec(stmt).first()
        if conversation:
            conversation.updated_at = datetime.utcnow()

        session.commit()
        session.refresh(message)
        return message

    def call_groq_with_tools(
        self,
        messages: List[Dict[str, str]],
        tools: List[Dict[str, Any]]
    ) -> tuple[str, List[Dict[str, Any]]]:
        """
        Call Groq API with tool definitions.

        Args:
            messages: Conversation history
            tools: Tool definitions

        Returns:
            Tuple of (response_text, tool_calls_info)
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tools,
                tool_choice="auto"
            )

            message = response.choices[0].message
            tool_calls_info = []

            # Handle tool calls if present
            if message.tool_calls:
                return message.content or "", [
                    {
                        "id": tc.id,
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    }
                    for tc in message.tool_calls
                ]

            return message.content or "", tool_calls_info

        except Exception as e:
            raise Exception(f"Groq API error: {str(e)}")

    def process_chat(
        self,
        session: Session,
        user_id: str,
        message: str,
        conversation_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Process a chat message and return the AI response.

        Args:
            session: Database session
            user_id: ID of the user
            message: User's message
            conversation_id: Optional existing conversation ID

        Returns:
            Dictionary with response, conversation_id, and tool_calls
        """
        print(f"[ChatService] Processing chat for user: {user_id}, conversation_id: {conversation_id}")

        # Get or create conversation
        conversation = self.get_or_create_conversation(
            session, user_id, conversation_id
        )

        # Save user message
        self.save_message(
            session, conversation.id, user_id, "user", message
        )

        # Get conversation history
        history = self.get_conversation_history(session, conversation.id)
        print(f"[ChatService] Conversation history length: {len(history)}")

        # Build messages for Groq API
        system_message = {
            "role": "system",
            "content": """You are a friendly and helpful todo list assistant for the TodoPro app.

YOUR MAIN JOB: Help users manage their tasks through natural conversation.

You have access to these tools:
- add_task: Create a new task
- list_tasks: View tasks (all, pending, or completed)
- complete_task: Mark a task as done
- delete_task: Remove a task
- update_task: Change a task's title or description

IMPORTANT RULES FOR TOOL CALLS:
1. ALWAYS use task_id as an INTEGER (number), never as a string. Example: {"task_id": 5} NOT {"task_id": "5"}
2. When user mentions a task by name (like "shopping"), first call list_tasks to find its ID, then use that numeric ID.
3. If user doesn't provide a task ID, ask them to specify which task by ID number.

HOW TO RESPOND:
1. If the user wants to do something with tasks (create, view, complete, delete, update), use the appropriate tool.
2. If the user says hello, hi, greetings, or similar, respond warmly: "Hello! 👋 I'm your task assistant. How can I help you today? You can ask me to add tasks, show your tasks, or manage existing ones."
3. If the user asks something unrelated to tasks (like weather, math, general questions, etc.), politely say: "I'm sorry, I can only help with managing your todo tasks. I can add tasks, show your tasks, mark them complete, or update them. What would you like to do?"
4. If the message is unclear, ask for clarification: "I'm not sure what you'd like to do. Try saying something like 'Add a task to buy groceries' or 'Show me my tasks'."

Keep responses short and friendly. Always be helpful!"""
        }

        messages = [system_message] + history

        # Get tool definitions
        tools = get_tool_definitions()

        # Call Groq API
        response_text, tool_calls = self.call_groq_with_tools(messages, tools)

        # Execute any tool calls
        executed_tools = []
        if tool_calls:
            import json

            for tc in tool_calls:
                try:
                    tool_name = tc["name"]

                    # Parse arguments safely
                    arguments = {}
                    if tc.get("arguments"):
                        try:
                            arguments = json.loads(tc["arguments"])
                        except (json.JSONDecodeError, TypeError):
                            # If arguments is already a dict or invalid JSON
                            if isinstance(tc["arguments"], dict):
                                arguments = tc["arguments"]
                            else:
                                print(f"[ChatService] Failed to parse arguments: {tc['arguments']}")
                                arguments = {}

                    # Execute the tool
                    result = execute_tool(session, user_id, tool_name, arguments)
                    executed_tools.append({
                        "tool_name": tool_name,
                        "arguments": arguments,
                        "result": result
                    })
                except Exception as e:
                    print(f"[ChatService] Error executing tool {tc.get('name', 'unknown')}: {e}")
                    executed_tools.append({
                        "tool_name": tc.get("name", "unknown"),
                        "arguments": {},
                        "result": {"success": False, "error": f"Tool execution failed: {str(e)}"}
                    })
                    continue

                # Add tool result to conversation for follow-up
                if result.get("success"):
                    # Generate friendly response based on tool result
                    if tool_name == "add_task":
                        response_text = f"I've created a new task '{result.get('title')}' for you."
                    elif tool_name == "list_tasks":
                        tasks = result.get("tasks", [])
                        if not tasks:
                            response_text = "You don't have any tasks yet. Would you like to add one?"
                        else:
                            task_list = "\n".join([
                                f"{t['id']}. {'[✓]' if t['completed'] else '[ ]'} {t['title']}"
                                for t in tasks
                            ])
                            response_text = f"Here are your tasks:\n{task_list}"
                    elif tool_name == "complete_task":
                        response_text = f"Great! I've marked task {result.get('task_id')} as complete."
                    elif tool_name == "delete_task":
                        response_text = f"I've deleted the task '{result.get('title')}'."
                    elif tool_name == "update_task":
                        response_text = f"I've updated the task to '{result.get('title')}'."
                else:
                    response_text = f"Sorry, I couldn't complete that action: {result.get('error')}"

        # Save assistant response
        self.save_message(
            session, conversation.id, user_id, "assistant", response_text
        )

        return {
            "conversation_id": conversation.id,
            "response": response_text,
            "tool_calls": executed_tools
        }

    def get_user_conversations(
        self,
        session: Session,
        user_id: str,
        limit: int = 20,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Get list of conversations for a user.

        Args:
            session: Database session
            user_id: ID of the user
            limit: Maximum number of conversations
            offset: Pagination offset

        Returns:
            List of conversation dictionaries
        """
        stmt = select(Conversation).where(
            Conversation.user_id == user_id
        ).order_by(Conversation.updated_at.desc()).offset(offset).limit(limit)

        conversations = session.exec(stmt).all()

        result = []
        for conv in conversations:
            # Count messages
            msg_stmt = select(Message).where(
                Message.conversation_id == conv.id
            )
            message_count = len(session.exec(msg_stmt).all())

            result.append({
                "id": conv.id,
                "created_at": conv.created_at.isoformat(),
                "updated_at": conv.updated_at.isoformat(),
                "message_count": message_count
            })

        return result

    def get_conversation(
        self,
        session: Session,
        user_id: str,
        conversation_id: int
    ) -> Optional[Dict[str, Any]]:
        """
        Get a specific conversation with messages.

        Args:
            session: Database session
            user_id: ID of the user
            conversation_id: ID of the conversation

        Returns:
            Conversation dictionary or None if not found
        """
        stmt = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        conversation = session.exec(stmt).first()

        if not conversation:
            return None

        messages = self.get_conversation_history(session, conversation_id)

        return {
            "conversation_id": conversation.id,
            "messages": [
                {
                    "id": i,
                    "role": m["role"],
                    "content": m["content"],
                    "created_at": conversation.updated_at.isoformat()
                }
                for i, m in enumerate(messages)
            ],
            "created_at": conversation.created_at.isoformat(),
            "updated_at": conversation.updated_at.isoformat()
        }

    def delete_conversation(
        self,
        session: Session,
        user_id: str,
        conversation_id: int
    ) -> bool:
        """
        Delete a conversation and all its messages.

        Args:
            session: Database session
            user_id: ID of the user
            conversation_id: ID of the conversation

        Returns:
            True if deleted, False if not found
        """
        stmt = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        conversation = session.exec(stmt).first()

        if not conversation:
            return False

        # Delete messages first
        msg_stmt = select(Message).where(
            Message.conversation_id == conversation_id
        )
        messages = session.exec(msg_stmt).all()
        for msg in messages:
            session.delete(msg)

        # Delete conversation
        session.delete(conversation)
        session.commit()

        return True


# Singleton instance
chat_service = ChatService()
