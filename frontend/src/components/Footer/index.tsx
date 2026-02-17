import React from 'react';

const Footer: React.FC = () => {
  return (
    <footer className="bg-gradient-to-r from-gray-800 to-gray-900 text-white py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="col-span-1 md:col-span-2">
            <h3 className="text-xl font-bold mb-4 text-indigo-300">TodoPro</h3>
            <p className="text-gray-300 mb-4">
              A modern, professional task management solution designed to boost your productivity
              and streamline your daily workflow. Stay organized, stay focused, stay ahead.
            </p>
            <div className="flex space-x-4">
              <a href="#" className="text-gray-300 hover:text-white transition duration-150 ease-in-out">
                Terms
              </a>
              <a href="#" className="text-gray-300 hover:text-white transition duration-150 ease-in-out">
                Privacy
              </a>
              <a href="#" className="text-gray-300 hover:text-white transition duration-150 ease-in-out">
                Contact
              </a>
            </div>
          </div>

          <div>
            <h4 className="text-lg font-semibold mb-4 text-indigo-300">Features</h4>
            <ul className="space-y-2">
              <li><a href="#" className="text-gray-300 hover:text-white transition duration-150 ease-in-out">Task Management</a></li>
              <li><a href="#" className="text-gray-300 hover:text-white transition duration-150 ease-in-out">Priority Setting</a></li>
              <li><a href="#" className="text-gray-300 hover:text-white transition duration-150 ease-in-out">Progress Tracking</a></li>
              <li><a href="#" className="text-gray-300 hover:text-white transition duration-150 ease-in-out">Collaboration</a></li>
            </ul>
          </div>

          <div>
            <h4 className="text-lg font-semibold mb-4 text-indigo-300">Support</h4>
            <ul className="space-y-2">
              <li><a href="#" className="text-gray-300 hover:text-white transition duration-150 ease-in-out">Help Center</a></li>
              <li><a href="#" className="text-gray-300 hover:text-white transition duration-150 ease-in-out">FAQs</a></li>
              <li><a href="#" className="text-gray-300 hover:text-white transition duration-150 ease-in-out">Contact Us</a></li>
              <li><a href="#" className="text-gray-300 hover:text-white transition duration-150 ease-in-out">Community</a></li>
            </ul>
          </div>
        </div>

        <div className="mt-8 pt-8 border-t border-gray-700 text-center text-gray-400">
          <p>&copy; {new Date().getFullYear()} TodoPro. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;