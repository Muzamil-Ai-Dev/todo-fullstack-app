import React from 'react';
import { Task } from '@/components/TaskForm/TaskForm.types';
import { formatDateOnly } from '@/utils/dateUtils';

interface TodoItemProps {
  task: Task;
  onToggleComplete: (id: number) => void;
  onDelete: (id: number) => void;
  onEdit: (task: Task) => void;
}

const TodoItem: React.FC<TodoItemProps> = ({ task, onToggleComplete, onDelete, onEdit }) => {
  const formatDate = (dateString: string) => {
    return formatDateOnly(dateString);
  };

  return (
    <div className={`bg-white rounded-xl shadow-md p-5 mb-4 transition-all duration-300 hover:shadow-lg border-l-4 ${
      task.completed
        ? 'border-green-500 bg-green-50'
        : 'border-indigo-500 hover:border-indigo-600'
    }`}>
      <div className="flex items-start justify-between">
        <div className="flex items-start space-x-3">
          <input
            type="checkbox"
            checked={task.completed}
            onChange={() => onToggleComplete(task.id)}
            className={`h-5 w-5 mt-1 rounded-full border-2 cursor-pointer ${
              task.completed
                ? 'bg-green-500 border-green-500'
                : 'bg-white border-gray-300 hover:border-indigo-400'
            }`}
          />
          <div>
            <h3 className={`font-semibold text-lg ${
              task.completed
                ? 'text-gray-500 line-through'
                : 'text-gray-900'
            }`}>
              {task.title}
            </h3>
            {task.description && (
              <p className={`mt-2 text-gray-700 ${
                task.completed ? 'line-through' : ''
              }`}>
                {task.description}
              </p>
            )}
            <div className="mt-3 flex items-center text-xs text-gray-500">
              {task.updated_at !== task.created_at ? (
                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full bg-blue-100 text-blue-800">
                  <svg className="-ml-0.5 mr-1.5 h-2 w-2 text-blue-500" fill="currentColor" viewBox="0 0 8 8">
                    <circle cx="4" cy="4" r="3" />
                  </svg>
                  Updated: {new Date(task.updated_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
                </span>
              ) : (
                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full bg-gray-100">
                  <svg className="-ml-0.5 mr-1.5 h-2 w-2 text-gray-400" fill="currentColor" viewBox="0 0 8 8">
                    <circle cx="4" cy="4" r="3" />
                  </svg>
                  Created: {new Date(task.created_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
                </span>
              )}
            </div>
          </div>
        </div>
        <div className="flex space-x-2">
          <button
            onClick={() => onEdit(task)}
            className="p-2 rounded-full hover:bg-blue-100 text-blue-600 hover:text-blue-800 transition duration-150 ease-in-out"
            aria-label="Edit task"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
            </svg>
          </button>
          <button
            onClick={() => onDelete(task.id)}
            className="p-2 rounded-full hover:bg-red-100 text-red-600 hover:text-red-800 transition duration-150 ease-in-out"
            aria-label="Delete task"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
          </button>
        </div>
      </div>

      {!task.completed && (
        <div className="mt-4 pt-4 border-t border-gray-100">
          <div className="flex items-center justify-between">
            <div className="text-sm text-gray-500">Progress</div>
            <div className="w-3/4 bg-gray-200 rounded-full h-2">
              <div
                className={`h-2 rounded-full ${
                  task.completed ? 'bg-green-500' : 'bg-indigo-500'
                }`}
                style={{ width: task.completed ? '100%' : '30%' }}
              ></div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default TodoItem;