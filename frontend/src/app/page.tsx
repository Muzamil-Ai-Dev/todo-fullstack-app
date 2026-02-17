'use client';

import React from 'react';
import Link from 'next/link';
import { useAuth } from '@/context/AuthContext';

const HomePage: React.FC = () => {
  const { isAuthenticated, loading } = useAuth();

  // If still loading, show nothing or a loading state
  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-white">
      <div className="relative overflow-hidden">
        <div className="max-w-[90%] md:max-w-5xl lg:max-w-6xl xl:max-w-7xl 2xl:max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="relative z-10 pb-8 bg-white sm:pb-16 md:pb-20 lg:pb-28 xl:pb-32">
            <main className="mt-16 mx-auto max-w-4xl sm:mt-20 md:mt-24 lg:mt-28 xl:mt-32 px-4">
              <div className="flex flex-col items-center text-center space-y-6 sm:space-y-8">
                <h1 className="text-4xl leading-tight font-extrabold text-gray-900 sm:text-5xl md:text-6xl max-w-4xl">
                  <span className="block">Boost your productivity with</span>{' '}
                  <span className="block text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-purple-600">TodoPro</span>
                </h1>
                <p className="mt-4 text-base text-gray-600 max-w-2xl mx-auto sm:mt-6 sm:text-lg md:mt-6 md:text-xl lg:mt-8 lg:text-xl xl:text-2xl">
                  A professional task management solution designed to streamline your workflow and help you stay organized.
                  Join thousands of users who trust our platform for their daily productivity needs.
                </p>
                {!isAuthenticated ? (
                  <div className="mt-8 sm:mt-10 flex flex-col sm:flex-row items-center justify-center gap-5 w-full max-w-sm sm:max-w-md md:max-w-lg lg:max-w-xl">
                    <div className="w-full sm:w-auto">
                      <Link
                        href="/register"
                        className="w-full sm:w-auto flex items-center justify-center px-6 py-3 sm:px-7 sm:py-4 md:px-8 md:py-4 border border-transparent text-base sm:text-lg md:text-xl font-bold rounded-xl text-white bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 transition duration-300 ease-in-out transform hover:-translate-y-0.5 hover:shadow-2xl"
                      >
                        <span className="mr-2 text-lg sm:text-xl">🚀</span> Get Started Free
                      </Link>
                    </div>
                    <div className="w-full sm:w-auto">
                      <Link
                        href="/login"
                        className="w-full sm:w-auto flex items-center justify-center px-6 py-3 sm:px-7 sm:py-4 md:px-8 md:py-4 border-2 border-indigo-600 text-base sm:text-lg md:text-xl font-bold rounded-xl text-indigo-700 bg-white hover:bg-indigo-50 transition duration-300 ease-in-out transform hover:-translate-y-0.5 hover:shadow-lg"
                      >
                        <span className="mr-2 text-lg sm:text-xl">👋</span> Sign In
                      </Link>
                    </div>
                  </div>
                ) : (
                  <div className="mt-8 sm:mt-10 flex flex-col sm:flex-row items-center justify-center gap-5 w-full max-w-sm sm:max-w-md md:max-w-lg">
                    <div className="w-full sm:w-auto">
                      <Link
                        href="/dashboard"
                        className="w-full sm:w-auto flex items-center justify-center px-6 py-3 sm:px-7 sm:py-4 md:px-8 md:py-4 border border-transparent text-base sm:text-lg md:text-xl font-bold rounded-xl text-white bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 transition duration-300 ease-in-out transform hover:-translate-y-0.5 hover:shadow-2xl"
                      >
                        <span className="mr-2 text-lg sm:text-xl">🏠</span> Go to Dashboard
                      </Link>
                    </div>
                  </div>
                )}
              </div>
            </main>

            {/* Features section */}
            <section className="mt-16 sm:mt-20 mx-auto max-w-6xl px-4 sm:px-6 lg:px-8 bg-white pt-10 sm:pt-16">
              <h2 className="text-2xl sm:text-3xl md:text-4xl font-bold text-center text-gray-900 mb-10 sm:mb-16">Why Choose TodoPro?</h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8 lg:gap-10">
                <div className="bg-white rounded-2xl shadow-lg p-5 sm:p-6 hover:shadow-xl transition-shadow duration-300 flex flex-col min-h-[200px] sm:min-h-[220px] border border-gray-100">
                  <div className="w-12 h-12 rounded-full bg-indigo-100 flex items-center justify-center mb-4 self-center flex-shrink-0">
                    <span className="text-lg sm:text-xl md:text-2xl">✅</span>
                  </div>
                  <h3 className="text-base sm:text-lg md:text-xl font-bold text-gray-900 mb-3 text-center flex-grow">Easy Task Management</h3>
                  <p className="text-gray-600 text-xs sm:text-sm md:text-base mt-auto text-center">Organize your tasks effortlessly with our intuitive interface and smart features.</p>
                </div>

                <div className="bg-white rounded-2xl shadow-lg p-5 sm:p-6 hover:shadow-xl transition-shadow duration-300 flex flex-col min-h-[200px] sm:min-h-[220px] border border-gray-100">
                  <div className="w-12 h-12 rounded-full bg-indigo-100 flex items-center justify-center mb-4 self-center flex-shrink-0">
                    <span className="text-lg sm:text-xl md:text-2xl">🔒</span>
                  </div>
                  <h3 className="text-base sm:text-lg md:text-xl font-bold text-gray-900 mb-3 text-center flex-grow">Secure & Private</h3>
                  <p className="text-gray-600 text-xs sm:text-sm md:text-base mt-auto text-center">Your data is protected with enterprise-grade security and privacy measures.</p>
                </div>

                <div className="bg-white rounded-2xl shadow-lg p-5 sm:p-6 hover:shadow-xl transition-shadow duration-300 flex flex-col min-h-[200px] sm:min-h-[220px] border border-gray-100">
                  <div className="w-12 h-12 rounded-full bg-indigo-100 flex items-center justify-center mb-4 self-center flex-shrink-0">
                    <span className="text-lg sm:text-xl md:text-2xl">📱</span>
                  </div>
                  <h3 className="text-base sm:text-lg md:text-xl font-bold text-gray-900 mb-3 text-center flex-grow">Always Accessible</h3>
                  <p className="text-gray-600 text-xs sm:text-sm md:text-base mt-auto text-center">Access your tasks from anywhere, anytime, on any device.</p>
                </div>
              </div>
            </section>

            {/* Detailed Features Section */}
            <section className="mt-20 sm:mt-24 mx-auto max-w-6xl px-4 sm:px-6 lg:px-8 bg-white py-12 sm:py-16 rounded-3xl shadow-lg">
              <h2 className="text-3xl sm:text-4xl font-bold text-center text-gray-900 mb-12">Powerful Features for Maximum Productivity</h2>

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-10 sm:gap-12">
                {/* Task Management */}
                <div className="bg-gradient-to-br from-indigo-50 to-white p-6 sm:p-8 rounded-2xl shadow-md border border-gray-100">
                  <div className="flex items-center mb-5">
                    <div className="w-12 h-12 rounded-full bg-indigo-100 flex items-center justify-center mr-4 flex-shrink-0">
                      <span className="text-xl text-indigo-700">✅</span>
                    </div>
                    <h3 className="text-2xl font-bold text-gray-900">Task Management</h3>
                  </div>
                  <p className="text-gray-600 mb-6 leading-relaxed">
                    Streamline your workflow with our intuitive task management system. Create, organize, and prioritize tasks with ease.
                  </p>

                  <div className="bg-white p-4 rounded-xl border border-gray-200">
                    <h4 className="font-semibold text-gray-800 mb-3">Workflow:</h4>
                    <ol className="list-decimal list-inside space-y-2 text-gray-700">
                      <li className="flex items-start">
                        <span className="text-indigo-600 font-medium mr-2">1.</span>
                        <span>Create new tasks with titles, descriptions, and deadlines</span>
                      </li>
                      <li className="flex items-start">
                        <span className="text-indigo-600 font-medium mr-2">2.</span>
                        <span>Organize tasks into categories or projects</span>
                      </li>
                      <li className="flex items-start">
                        <span className="text-indigo-600 font-medium mr-2">3.</span>
                        <span>Set priorities and due dates for effective planning</span>
                      </li>
                      <li className="flex items-start">
                        <span className="text-indigo-600 font-medium mr-2">4.</span>
                        <span>Track progress and mark tasks as complete</span>
                      </li>
                      <li className="flex items-start">
                        <span className="text-indigo-600 font-medium mr-2">5.</span>
                        <span>Review and analyze your productivity patterns</span>
                      </li>
                    </ol>
                  </div>
                </div>

                {/* Priority Setting */}
                <div className="bg-gradient-to-br from-purple-50 to-white p-6 sm:p-8 rounded-2xl shadow-md border border-gray-100">
                  <div className="flex items-center mb-5">
                    <div className="w-12 h-12 rounded-full bg-purple-100 flex items-center justify-center mr-4 flex-shrink-0">
                      <span className="text-xl text-purple-700">⚡</span>
                    </div>
                    <h3 className="text-2xl font-bold text-gray-900">Priority Setting</h3>
                  </div>
                  <p className="text-gray-600 mb-6 leading-relaxed">
                    Focus on what matters most with our smart priority system. Never miss important deadlines again.
                  </p>
                  <ul className="space-y-3 text-gray-700">
                    <li className="flex items-start">
                      <span className="text-purple-600 font-medium mr-3">•</span>
                      <span>Set priority levels (High, Medium, Low) for each task</span>
                    </li>
                    <li className="flex items-start">
                      <span className="text-purple-600 font-medium mr-3">•</span>
                      <span>Visual indicators highlight urgent tasks</span>
                    </li>
                    <li className="flex items-start">
                      <span className="text-purple-600 font-medium mr-3">•</span>
                      <span>Automatic sorting by priority and deadline</span>
                    </li>
                    <li className="flex items-start">
                      <span className="text-purple-600 font-medium mr-3">•</span>
                      <span>Priority-based notifications and reminders</span>
                    </li>
                  </ul>
                </div>

                {/* Progress Tracking */}
                <div className="bg-gradient-to-br from-blue-50 to-white p-6 sm:p-8 rounded-2xl shadow-md border border-gray-100">
                  <div className="flex items-center mb-5">
                    <div className="w-12 h-12 rounded-full bg-blue-100 flex items-center justify-center mr-4 flex-shrink-0">
                      <span className="text-xl text-blue-700">📊</span>
                    </div>
                    <h3 className="text-2xl font-bold text-gray-900">Progress Tracking</h3>
                  </div>
                  <p className="text-gray-600 mb-6 leading-relaxed">
                    Monitor your achievements and stay motivated with comprehensive progress insights.
                  </p>
                  <ul className="space-y-3 text-gray-700">
                    <li className="flex items-start">
                      <span className="text-blue-600 font-medium mr-3">•</span>
                      <span>Real-time progress visualization with charts</span>
                    </li>
                    <li className="flex items-start">
                      <span className="text-blue-600 font-medium mr-3">•</span>
                      <span>Daily, weekly, and monthly productivity reports</span>
                    </li>
                    <li className="flex items-start">
                      <span className="text-blue-600 font-medium mr-3">•</span>
                      <span>Completion rate tracking and statistics</span>
                    </li>
                    <li className="flex items-start">
                      <span className="text-blue-600 font-medium mr-3">•</span>
                      <span>Goal-setting and milestone achievement tracking</span>
                    </li>
                  </ul>
                </div>

                {/* Collaboration */}
                <div className="bg-gradient-to-br from-green-50 to-white p-6 sm:p-8 rounded-2xl shadow-md border border-gray-100">
                  <div className="flex items-center mb-5">
                    <div className="w-12 h-12 rounded-full bg-green-100 flex items-center justify-center mr-4 flex-shrink-0">
                      <span className="text-xl text-green-700">👥</span>
                    </div>
                    <h3 className="text-2xl font-bold text-gray-900">Collaboration</h3>
                  </div>
                  <p className="text-gray-600 mb-6 leading-relaxed">
                    Work seamlessly with your team and stay connected across all your projects.
                  </p>
                  <ul className="space-y-3 text-gray-700">
                    <li className="flex items-start">
                      <span className="text-green-600 font-medium mr-3">•</span>
                      <span>Invite team members and assign tasks</span>
                    </li>
                    <li className="flex items-start">
                      <span className="text-green-600 font-medium mr-3">•</span>
                      <span>Real-time task updates and notifications</span>
                    </li>
                    <li className="flex items-start">
                      <span className="text-green-600 font-medium mr-3">•</span>
                      <span>Shared project boards and progress tracking</span>
                    </li>
                    <li className="flex items-start">
                      <span className="text-green-600 font-medium mr-3">•</span>
                      <span>Commenting and feedback system</span>
                    </li>
                  </ul>
                </div>
              </div>
            </section>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;