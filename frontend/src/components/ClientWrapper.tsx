'use client';

import { AuthProvider } from '@/context/AuthContext';
import React, { ReactNode } from 'react';

interface ClientWrapperProps {
  children: ReactNode;
}

export default function ClientWrapper({ children }: ClientWrapperProps) {
  return (
    <AuthProvider>
      {children}
    </AuthProvider>
  );
}