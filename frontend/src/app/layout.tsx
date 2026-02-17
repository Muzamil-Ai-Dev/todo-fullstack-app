import React from 'react';
import '@/styles/globals.css'; // Import global styles
import ClientRoot from './ClientRoot';
import Header from '@/components/Header';
import Footer from '@/components/Footer';

export const metadata = {
  title: 'TodoPro - Professional Task Management',
  description: 'Full-Stack Todo Application with Next.js and FastAPI',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gray-50">
        <ClientRoot>
          <Header />
          <main>
            {children}
          </main>
          <Footer />
        </ClientRoot>
      </body>
    </html>
  );
}