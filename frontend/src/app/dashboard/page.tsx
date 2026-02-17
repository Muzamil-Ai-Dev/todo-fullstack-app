'use client';

import React from 'react';
import ProtectedRoute from '../../components/ProtectedRoute';
import TaskManager from '../../components/TaskManager/TaskManager';

const DashboardPage: React.FC = () => {
  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gray-50">
        <TaskManager />
      </div>
    </ProtectedRoute>
  );
};

export default DashboardPage;