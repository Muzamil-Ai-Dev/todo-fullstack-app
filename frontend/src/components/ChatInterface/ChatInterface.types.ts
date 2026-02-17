/**
 * Types for the ChatInterface component
 */

export interface Message {
  id: number;
  role: 'user' | 'assistant';
  content: string;
  created_at: string;
}

export interface ToolCallInfo {
  tool_name: string;
  arguments: Record<string, unknown>;
  result: Record<string, unknown>;
}

export interface ChatResponse {
  conversation_id: number;
  response: string;
  tool_calls: ToolCallInfo[];
}

export interface ConversationHistory {
  conversation_id: number;
  messages: Message[];
  created_at: string;
  updated_at: string;
}

export interface ConversationListItem {
  id: number;
  created_at: string;
  updated_at: string;
  message_count: number;
}

export interface ChatInterfaceProps {
  conversationId?: number;
  onConversationChange?: (conversationId: number) => void;
}
