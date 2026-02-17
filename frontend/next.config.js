/** @type {import('next').NextConfig} */
const isProd = process.env.NODE_ENV === 'production';
const repoName = 'todo-fullstack-app'; // GitHub repository name

const nextConfig = {
  // Enable static export for GitHub Pages
  output: 'export',

  // Set basePath for GitHub Pages deployment
  basePath: isProd ? `/${repoName}` : '',

  // Disable image optimization for static export
  images: {
    unoptimized: true,
  },

  // Trailing slashes for GitHub Pages compatibility
  trailingSlash: true,

  // Environment variables
  env: {
    NEXT_PUBLIC_API_BASE_URL: process.env.NEXT_PUBLIC_API_BASE_URL,
    NEXT_PUBLIC_BACKEND_URL: process.env.NEXT_PUBLIC_BACKEND_URL,
  },
};

module.exports = nextConfig;