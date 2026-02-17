'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { useAuth } from '@/context/AuthContext';
import UserAvatar from '../UserAvatar';

const Header: React.FC = () => {
  const { user, logout } = useAuth();
  const [showConfirmDialog, setShowConfirmDialog] = useState(false);

  const handleLogout = async () => {
    try {
      await logout();
      setShowConfirmDialog(false);
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  const handleConfirmLogout = () => {
    setShowConfirmDialog(true);
  };

  const handleCancelLogout = () => {
    setShowConfirmDialog(false);
  };

  return (
    <header className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center">
            <Link href="/" className="flex-shrink-0 flex items-center">
              <div className="bg-white text-indigo-600 font-bold text-xl px-3 py-2 rounded-lg shadow-md">
                TodoPro
              </div>
            </Link>
            <nav className="hidden md:block ml-10">
              <div className="flex items-baseline space-x-4">
                <Link
                  href="/"
                  className="px-3 py-2 rounded-md text-sm font-medium text-white hover:bg-indigo-700 transition duration-150 ease-in-out"
                >
                  Home
                </Link>
                <Link
                  href="/dashboard"
                  className="px-3 py-2 rounded-md text-sm font-medium text-white hover:bg-indigo-700 transition duration-150 ease-in-out"
                >
                  Dashboard
                </Link>
              </div>
            </nav>
          </div>

          <div className="flex items-center space-x-4">
            {user ? (
              <div className="flex items-center space-x-3">
                <div className="relative">
                  <UserAvatar
                    email={user.email || user.username || 'user@example.com'}
                    size="md"
                  />
                </div>
                <button
                  onClick={handleConfirmLogout}
                  className="px-4 py-2 rounded-md text-sm font-medium bg-white text-indigo-600 hover:bg-indigo-50 transition duration-150 ease-in-out"
                >
                  Logout
                </button>
              </div>
            ) : (
              <div className="flex space-x-2">
                <Link
                  href="/login"
                  className="px-4 py-2 rounded-md text-sm font-medium bg-white text-indigo-600 hover:bg-indigo-50 transition duration-150 ease-in-out"
                >
                  Sign In
                </Link>
                <Link
                  href="/register"
                  className="px-4 py-2 rounded-md text-sm font-medium bg-indigo-700 text-white hover:bg-indigo-800 transition duration-150 ease-in-out"
                >
                  Sign Up
                </Link>
              </div>
            )}
          </div>
        </div>

        {/* Confirmation Dialog */}
        {showConfirmDialog && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-xl p-6 max-w-md w-full mx-4 shadow-2xl">
              <h3 className="text-xl font-bold text-gray-900 mb-3">Confirm Logout</h3>
              <p className="text-gray-600 mb-6">Are you sure you want to log out? You'll need to sign in again to access your account.</p>

              <div className="flex justify-end space-x-3">
                <button
                  onClick={handleCancelLogout}
                  className="px-4 py-2 rounded-md text-sm font-medium text-gray-700 bg-gray-200 hover:bg-gray-300 transition duration-150 ease-in-out"
                >
                  Cancel
                </button>
                <button
                  onClick={handleLogout}
                  className="px-4 py-2 rounded-md text-sm font-medium bg-indigo-600 text-white hover:bg-indigo-700 transition duration-150 ease-in-out"
                >
                  Yes, Log Out
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;