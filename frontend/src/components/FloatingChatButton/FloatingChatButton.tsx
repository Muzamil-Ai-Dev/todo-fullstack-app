'use client';

import React, { useState, useRef, useEffect, useCallback } from 'react';
import { useAuth } from '@/context/AuthContext';
import { MessageBubble } from '../MessageBubble/MessageBubble';
import { Message, ChatResponse } from '../ChatInterface/ChatInterface.types';
import { sendMessage } from '@/services/api';

const STORAGE_KEY_PREFIX = 'chat_conversation_';

export const FloatingChatButton: React.FC = () => {
  const { user } = useAuth();
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [conversationId, setConversationId] = useState<number | undefined>();
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  // Get storage key for user
  const getStorageKey = useCallback(() => {
    if (!user) return null;
    return `${STORAGE_KEY_PREFIX}${user.id}`;
  }, [user]);

  // Load conversation from localStorage on mount or when user changes
  useEffect(() => {
    const storageKey = getStorageKey();
    if (storageKey && user) {
      try {
        const saved = localStorage.getItem(storageKey);
        if (saved) {
          const data = JSON.parse(saved);
          setMessages(data.messages || []);
          setConversationId(data.conversationId);
        } else {
          // No saved data for this user, clear state
          setMessages([]);
          setConversationId(undefined);
        }
      } catch (e) {
        console.error('Failed to load conversation:', e);
        setMessages([]);
        setConversationId(undefined);
      }
    } else {
      // No user, clear state
      setMessages([]);
      setConversationId(undefined);
    }
  }, [getStorageKey, user]);

  // Save conversation to localStorage when messages change
  useEffect(() => {
    const storageKey = getStorageKey();
    if (storageKey && messages.length > 0) {
      try {
        localStorage.setItem(storageKey, JSON.stringify({
          messages,
          conversationId
        }));
      } catch (e) {
        console.error('Failed to save conversation:', e);
      }
    }
  }, [messages, conversationId, getStorageKey]);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Focus input when chat opens
  useEffect(() => {
    if (isOpen) {
      inputRef.current?.focus();
    }
  }, [isOpen]);

  // Only show the button if user is logged in
  if (!user) {
    return null;
  }

  // Dispatch custom event when tasks are modified
  const dispatchTasksChanged = (action: string) => {
    if (typeof window !== 'undefined') {
      window.dispatchEvent(new CustomEvent('tasksChanged', { detail: { action } }));
    }
  };

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = inputValue.trim();
    setInputValue('');
    setError(null);

    // Add user message to UI immediately
    const tempUserMessage: Message = {
      id: Date.now(),
      role: 'user',
      content: userMessage,
      created_at: new Date().toISOString()
    };
    setMessages((prev) => [...prev, tempUserMessage]);
    setIsLoading(true);

    try {
      const response: ChatResponse = await sendMessage(
        userMessage,
        conversationId
      );

      // Update conversation ID if this is a new conversation
      if (!conversationId && response.conversation_id) {
        setConversationId(response.conversation_id);
      }

      // Add assistant response to UI
      const assistantMessage: Message = {
        id: Date.now() + 1,
        role: 'assistant',
        content: response.response,
        created_at: new Date().toISOString()
      };
      setMessages((prev) => [...prev, assistantMessage]);

      // Check if tasks were modified and dispatch event
      if (response.tool_calls && response.tool_calls.length > 0) {
        const actions = response.tool_calls.map(tc => tc.tool_name);
        if (actions.some(a => ['add_task', 'complete_task', 'delete_task', 'update_task'].includes(a))) {
          dispatchTasksChanged(actions[0]);
        }
      }
    } catch (err) {
      console.error('Error sending message:', err);

      // If there's a server error, try again without conversation ID (start fresh)
      if (conversationId) {
        console.log('Retrying without conversation ID...');
        setConversationId(undefined);
        try {
          const retryResponse: ChatResponse = await sendMessage(userMessage, undefined);
          if (retryResponse.conversation_id) {
            setConversationId(retryResponse.conversation_id);
          }
          const assistantMessage: Message = {
            id: Date.now() + 1,
            role: 'assistant',
            content: retryResponse.response,
            created_at: new Date().toISOString()
          };
          setMessages((prev) => [...prev, assistantMessage]);

          if (retryResponse.tool_calls && retryResponse.tool_calls.length > 0) {
            const actions = retryResponse.tool_calls.map(tc => tc.tool_name);
            if (actions.some(a => ['add_task', 'complete_task', 'delete_task', 'update_task'].includes(a))) {
              dispatchTasksChanged(actions[0]);
            }
          }
          setIsLoading(false);
          return;
        } catch (retryErr) {
          console.error('Retry also failed:', retryErr);
        }
      }

      setError(
        err instanceof Error
          ? err.message
          : 'Failed to send message. Please try again.'
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  const closeChat = () => {
    setIsOpen(false);
  };

  const clearConversation = () => {
    setMessages([]);
    setConversationId(undefined);
    const storageKey = getStorageKey();
    if (storageKey) {
      localStorage.removeItem(storageKey);
    }
  };

  return (
    <>
      {/* Chat Widget Popup - Responsive for all devices */}
      {isOpen && (
        <div className="fixed z-50 flex flex-col overflow-hidden bg-white border border-gray-200 shadow-2xl rounded-2xl animate-in slide-in-from-bottom-4 fade-in duration-300
          /* Mobile: Full width at bottom */
          bottom-0 left-0 right-0 h-[60vh] rounded-b-none rounded-t-2xl
          /* Tablet and larger: Smaller floating widget */
          sm:bottom-20 sm:left-auto sm:right-6 sm:w-80 sm:h-[420px] sm:rounded-2xl
        ">
          {/* Header */}
          <div className="flex items-center justify-between px-4 py-2.5 text-white bg-gradient-to-r from-indigo-600 to-purple-600">
            <div className="flex items-center gap-2">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
              <span className="text-sm font-semibold">AI Assistant</span>
            </div>
            <div className="flex items-center gap-1">
              {messages.length > 0 && (
                <button
                  onClick={clearConversation}
                  className="p-1 transition-colors rounded-full hover:bg-white/20"
                  aria-label="Clear conversation"
                  title="New chat"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                  </svg>
                </button>
              )}
              <button
                onClick={closeChat}
                className="p-1 transition-colors rounded-full hover:bg-white/20"
                aria-label="Close chat"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>

          {/* Messages */}
          <div className="flex-1 p-2.5 space-y-2 overflow-y-auto bg-gray-50">
            {messages.length === 0 && (
              <div className="mt-6 text-center text-gray-500">
                <p className="mb-1 text-sm">Hi! I&apos;m your task assistant.</p>
                <p className="text-xs">Try: &quot;Add a task to buy groceries&quot;</p>
              </div>
            )}

            {messages.map((message) => (
              <MessageBubble
                key={message.id}
                role={message.role}
                content={message.content}
                timestamp={message.created_at}
              />
            ))}

            {isLoading && (
              <div className="flex justify-start mb-2">
                <div className="px-3 py-2 bg-gray-100 rounded-lg">
                  <div className="flex items-center space-x-1">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }} />
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Error */}
          {error && (
            <div className="px-3 py-1 bg-red-50 border-t border-red-200">
              <p className="text-xs text-red-600">{error}</p>
            </div>
          )}

          {/* Input */}
          <div className="p-2.5 bg-white border-t border-gray-200">
            <div className="flex items-end space-x-2">
              <textarea
                ref={inputRef}
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Type a message..."
                disabled={isLoading}
                maxLength={500}
                rows={1}
                className="flex-1 px-3 py-2 text-sm border border-gray-300 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent disabled:opacity-50 max-h-20"
              />
              <button
                onClick={handleSendMessage}
                disabled={!inputValue.trim() || isLoading}
                className="p-2 text-white transition-all rounded-lg bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                </svg>
              </button>
            </div>
            <p className="mt-1 text-right text-[10px] text-gray-400">
              {inputValue.length}/500
            </p>
          </div>
        </div>
      )}

      {/* Floating Button */}
      <button
        onClick={toggleChat}
        className={`fixed z-50 flex items-center justify-center w-12 h-12 rounded-full shadow-lg transition-all duration-300 group
          /* Mobile: Smaller and closer to edge */
          bottom-4 right-4
          /* Tablet and larger: Standard position */
          sm:bottom-5 sm:right-5 sm:w-14 sm:h-14
          ${isOpen
            ? 'bg-gray-700 hover:bg-gray-800 rotate-0'
            : 'bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 hover:scale-110'
          }`}
        aria-label={isOpen ? 'Close chat' : 'Open AI Chat'}
      >
        {isOpen ? (
          <svg className="w-5 h-5 text-white sm:w-6 sm:h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        ) : (
          <>
            <svg className="w-5 h-5 text-white sm:w-6 sm:h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
            </svg>
            {/* Tooltip - hidden on mobile */}
            <span className="absolute right-14 px-2 py-1 text-xs text-white bg-gray-900 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity duration-200 whitespace-nowrap pointer-events-none hidden sm:block">
              AI Assistant
            </span>
          </>
        )}
      </button>
    </>
  );
};

export default FloatingChatButton;
