'use client';

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import dynamic from 'next/dynamic';

// Dynamically import ChatInterface to avoid SSR issues
const ChatInterface = dynamic(
  () => import('@/components/ChatInterface').then((mod) => mod.ChatInterface),
  { ssr: false }
);

export default function ChatPage() {
  const router = useRouter();
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);

  useEffect(() => {
    // Check if user is authenticated
    const token = localStorage.getItem('access_token');
    if (!token) {
      router.push('/login');
    } else {
      setIsAuthenticated(true);
    }
  }, [router]);

  if (isAuthenticated === null) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null; // Will redirect to login
  }

  return (
    <div className="container mx-auto px-4 py-6 max-w-4xl">
      {/* Page header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">AI Task Assistant</h1>
        <p className="text-gray-600 mt-1">
          Chat with me to manage your tasks using natural language
        </p>
      </div>

      {/* Chat container */}
      <div className="bg-white rounded-lg shadow-lg overflow-hidden border border-gray-200">
        <div className="h-[60vh] sm:h-[65vh] md:h-[70vh]">
          <ChatInterface />
        </div>
      </div>

      {/* Helper text */}
      <div className="mt-4 text-center text-sm text-gray-500">
        <p>
          Try saying: &quot;Add a task to buy groceries&quot;, &quot;Show me my tasks&quot;, or &quot;Mark task 1 as complete&quot;
        </p>
      </div>
    </div>
  );
}
