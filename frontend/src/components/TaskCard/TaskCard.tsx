import React from 'react';
import { Task } from './TaskCard.types';
import { formatDateOnly } from '@/utils/dateUtils';

interface TaskCardProps {
  task: Task;
  onToggleComplete: (id: number) => void;
  onDelete: (id: number) => void;
  onEdit: (task: Task) => void;
}

const TaskCard: React.FC<TaskCardProps> = ({ task, onToggleComplete, onDelete, onEdit }) => {
  return (
    <div className={`border rounded-lg p-4 mb-2 flex items-center justify-between ${task.completed ? 'bg-green-50' : 'bg-white'}`}>
      <div className="flex items-center">
        <input
          type="checkbox"
          checked={task.completed}
          onChange={() => onToggleComplete(task.id)}
          className="mr-2 h-4 w-4"
        />
        <div>
          <h3 className={`font-medium ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
            {task.title}
          </h3>
          {task.description && (
            <p className={`text-sm ${task.completed ? 'line-through text-gray-500' : 'text-gray-600'}`}>
              {task.description}
            </p>
          )}
          <div className="mt-2 flex items-center text-xs text-gray-500">
            {task.updated_at !== task.created_at ? (
              <span className="inline-flex items-center px-2 py-0.5 rounded-full bg-blue-100 text-blue-800">
                <svg className="-ml-0.5 mr-1 h-2 w-2 text-blue-500" fill="currentColor" viewBox="0 0 8 8">
                  <circle cx="4" cy="4" r="3" />
                </svg>
                Updated: {new Date(task.updated_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
              </span>
            ) : (
              <span className="inline-flex items-center px-2 py-0.5 rounded-full bg-gray-100">
                <svg className="-ml-0.5 mr-1 h-2 w-2 text-gray-400" fill="currentColor" viewBox="0 0 8 8">
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
          className="text-blue-500 hover:text-blue-700 text-sm"
        >
          Edit
        </button>
        <button
          onClick={() => onDelete(task.id)}
          className="text-red-500 hover:text-red-700 text-sm"
        >
          Delete
        </button>
      </div>
    </div>
  );
};

export default TaskCard;