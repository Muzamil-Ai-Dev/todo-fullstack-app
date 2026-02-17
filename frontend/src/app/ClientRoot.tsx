'use client';

import React, { ReactNode } from 'react';
import { AuthProvider } from '@/context/AuthContext';
import FloatingChatButton from '@/components/FloatingChatButton';

interface ClientRootProps {
  children: ReactNode;
}

export default function ClientRoot({ children }: ClientRootProps) {
  return (
    <AuthProvider>
      {children}
      <FloatingChatButton />
    </AuthProvider>
  );
}