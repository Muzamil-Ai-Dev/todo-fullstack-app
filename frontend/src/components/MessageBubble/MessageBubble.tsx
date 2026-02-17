'use client';

import React from 'react';

interface MessageBubbleProps {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: string;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({
  role,
  content,
  timestamp
}) => {
  const isUser = role === 'user';

  return (
    <div
      className={`flex w-full mb-4 ${isUser ? 'justify-end' : 'justify-start'}`}
    >
      <div
        className={`max-w-[80%] rounded-lg px-4 py-3 ${
          isUser
            ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white'
            : 'bg-indigo-50 border border-indigo-100 text-gray-900'
        }`}
      >
        {/* Role indicator */}
        <div className="flex items-center mb-1">
          <span
            className={`text-xs font-medium ${
              isUser ? 'text-indigo-200' : 'text-indigo-600'
            }`}
          >
            {isUser ? 'You' : 'Assistant'}
          </span>
        </div>

        {/* Message content */}
        <p className="text-sm whitespace-pre-wrap break-words">{content}</p>

        {/* Timestamp */}
        {timestamp && (
          <span
            className={`text-xs mt-1 block ${
              isUser ? 'text-indigo-200' : 'text-gray-400'
            }`}
          >
            {new Date(timestamp).toLocaleTimeString([], {
              hour: '2-digit',
              minute: '2-digit'
            })}
          </span>
        )}
      </div>
    </div>
  );
};

export default MessageBubble;
