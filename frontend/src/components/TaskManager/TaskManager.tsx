import React, { useState, useEffect } from 'react';
import { Task } from '../TaskForm/TaskForm.types';
import TaskForm from '../TaskForm/TaskForm';
import TodoList from '../TodoList';
import { taskApi } from '../../services/api';
import { formatDateOnly } from '@/utils/dateUtils';

interface TaskManagerProps {}

const TaskManager: React.FC<TaskManagerProps> = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState<boolean>(false);
  const [editingTask, setEditingTask] = useState<Task | undefined>(undefined);
  const [filter, setFilter] = useState<'all' | 'pending' | 'completed'>('all');
  const [showDeleteConfirm, setShowDeleteConfirm] = useState<{show: boolean, taskId: number | null}>({show: false, taskId: null});

  // Fetch tasks from API
  useEffect(() => {
    const fetchTasks = async () => {
      try {
        setLoading(true);
        const response = await taskApi.getTasks(filter);
        setTasks(response.tasks || []);
      } catch (err) {
        setError('Failed to fetch tasks. Please try again.');
        console.error('Error fetching tasks:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchTasks();
  }, [filter]);

  const handleCreateTask = async (taskData: { title: string; description?: string }) => {
    try {
      const newTask = await taskApi.createTask(taskData.title, taskData.description);
      setTasks([newTask, ...tasks]);
      setShowForm(false);
    } catch (err) {
      setError('Failed to create task. Please try again.');
      console.error('Error creating task:', err);
    }
  };

  const handleUpdateTask = async (taskData: { title?: string; description?: string; completed?: boolean }) => {
    if (editingTask === undefined) return;

    try {
      const updatedTask = await taskApi.updateTask(
        editingTask.id,
        taskData.title,
        taskData.description,
        taskData.completed
      );

      setTasks(tasks.map(t => t.id === updatedTask.id ? updatedTask : t));
      setEditingTask(undefined);
      setShowForm(false);
    } catch (err) {
      setError('Failed to update task. Please try again.');
      console.error('Error updating task:', err);
    }
  };

  const handleToggleComplete = async (taskId: number) => {
    try {
      const updatedTask = await taskApi.toggleTaskCompletion(taskId);
      setTasks(tasks.map(t => t.id === taskId ? updatedTask : t));
    } catch (err) {
      setError('Failed to update task status. Please try again.');
      console.error('Error toggling task completion:', err);
    }
  };

  const handleDeleteTask = async (taskId: number) => {
    setShowDeleteConfirm({show: true, taskId});
  };

  const confirmDeleteTask = async () => {
    if (showDeleteConfirm.taskId === null) return;

    try {
      await taskApi.deleteTask(showDeleteConfirm.taskId);
      setTasks(tasks.filter(t => t.id !== showDeleteConfirm.taskId));
    } catch (err) {
      setError('Failed to delete task. Please try again.');
      console.error('Error deleting task:', err);
    } finally {
      setShowDeleteConfirm({show: false, taskId: null});
    }
  };

  const cancelDeleteTask = () => {
    setShowDeleteConfirm({show: false, taskId: null});
  };

  const handleEditTask = (task: Task) => {
    setEditingTask(task);
    setShowForm(true);
  };

  const handleFormSubmit = (taskData: { title: string; description?: string; completed?: boolean }) => {
    if (editingTask) {
      handleUpdateTask(taskData);
    } else {
      handleCreateTask(taskData);
    }
  };

  const handleCancelForm = () => {
    setShowForm(false);
    setEditingTask(undefined);
  };

  if (loading) {
    return (
      <div className="max-w-5xl mx-auto p-6">
        <div className="animate-pulse flex space-x-4">
          <div className="flex-1 space-y-4 py-1">
            <div className="h-8 bg-gray-200 rounded w-1/4"></div>
            <div className="space-y-2">
              <div className="h-4 bg-gray-200 rounded w-3/4"></div>
              <div className="h-4 bg-gray-200 rounded w-5/6"></div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto p-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8 gap-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-700 mt-2">Manage your tasks efficiently</p>
        </div>
        <button
          onClick={() => setShowForm(true)}
          className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-6 py-3 rounded-xl hover:from-indigo-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 shadow-md hover:shadow-lg transition duration-300 ease-in-out transform hover:-translate-y-0.5"
        >
          <div className="flex items-center space-x-2">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clipRule="evenodd" />
            </svg>
            <span>Add New Task</span>
          </div>
        </button>
      </div>

      {error && (
        <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-6 rounded">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <p className="text-sm text-red-800">{error}</p>
            </div>
          </div>
        </div>
      )}

      {showForm && (
        <div className="mb-8">
          <TaskForm
            onSubmit={handleFormSubmit}
            onCancel={handleCancelForm}
            task={editingTask}
          />
        </div>
      )}

      <TodoList
        tasks={tasks}
        onToggleComplete={handleToggleComplete}
        onDelete={handleDeleteTask}
        onEdit={handleEditTask}
        filter={filter}
        setFilter={setFilter}
      />

      {/* Delete Confirmation Dialog */}
      {showDeleteConfirm.show && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl p-6 max-w-md w-full mx-4 shadow-2xl">
            <h3 className="text-xl font-bold text-gray-900 mb-3">Confirm Delete</h3>
            <p className="text-gray-600 mb-6">Are you sure you want to delete this task? This action cannot be undone.</p>

            <div className="flex justify-end space-x-3">
              <button
                onClick={cancelDeleteTask}
                className="px-4 py-2 rounded-md text-sm font-medium text-gray-700 bg-gray-200 hover:bg-gray-300 transition duration-150 ease-in-out"
              >
                Cancel
              </button>
              <button
                onClick={confirmDeleteTask}
                className="px-4 py-2 rounded-md text-sm font-medium bg-red-600 text-white hover:bg-red-700 transition duration-150 ease-in-out"
              >
                Yes, Delete Task
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default TaskManager;