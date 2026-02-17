'use client';

import React, { ReactNode } from 'react';
import { AuthProvider } from '@/context/AuthContext';

interface ClientRootProps {
  children: ReactNode;
}

export default function ClientRoot({ children }: ClientRootProps) {
  return (
    <AuthProvider>
      {children}
    </AuthProvider>
  );
}