import React from 'react';

interface UserAvatarProps {
  email: string;
  size?: 'sm' | 'md' | 'lg';
}

const UserAvatar: React.FC<UserAvatarProps> = ({ email, size = 'md' }) => {
  // Extract initials from email (first two letters before @)
  const getInitials = (email: string) => {
    const username = email.split('@')[0];
    const parts = username.split('.');
    if (parts.length >= 2) {
      return (parts[0][0] + parts[1][0]).toUpperCase();
    } else {
      return username.substring(0, 2).toUpperCase();
    }
  };

  const initials = getInitials(email);

  // Generate a color based on the email for consistent coloring
  const getColor = (email: string) => {
    const colors = [
      'bg-indigo-100 text-indigo-800',
      'bg-blue-100 text-blue-800',
      'bg-green-100 text-green-800',
      'bg-yellow-100 text-yellow-800',
      'bg-purple-100 text-purple-800',
      'bg-pink-100 text-pink-800',
      'bg-red-100 text-red-800',
      'bg-gray-100 text-gray-800',
    ];

    let hash = 0;
    for (let i = 0; i < email.length; i++) {
      hash = email.charCodeAt(i) + ((hash << 5) - hash);
    }

    const index = Math.abs(hash) % colors.length;
    return colors[index];
  };

  const sizeClasses = {
    sm: 'w-8 h-8 text-xs',
    md: 'w-10 h-10 text-sm',
    lg: 'w-12 h-12 text-base',
  };

  return (
    <div
      className={`relative group ${sizeClasses[size]} ${getColor(email)} rounded-full flex items-center justify-center font-semibold cursor-pointer`}
      title={email}
    >
      {initials}
      {/* Tooltip that appears on hover for larger screens */}
      <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-2 bg-indigo-600 text-white text-xs rounded-lg shadow-lg opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none z-10 hidden lg:block whitespace-nowrap font-medium">
        {email}
      </div>
    </div>
  );
};

export default UserAvatar;