/** @type {import('next').NextConfig} */
const isProd = process.env.NODE_ENV === 'production';
const isGitHubPages = process.env.GITHUB_PAGES === 'true';
const repoName = 'todo-fullstack-app'; // GitHub repository name

const nextConfig = {
  // Enable static export only for GitHub Pages, standalone for Docker/Kubernetes
  ...(isGitHubPages ? { output: 'export' } : { output: 'standalone' }),

  // Set basePath for GitHub Pages deployment only
  basePath: isGitHubPages ? `/${repoName}` : '',

  // Disable image optimization for static export
  images: {
    unoptimized: isGitHubPages,
  },

  // Trailing slashes for GitHub Pages compatibility
  trailingSlash: isGitHubPages,

  // Environment variables
  env: {
    NEXT_PUBLIC_API_BASE_URL: process.env.NEXT_PUBLIC_API_BASE_URL,
    NEXT_PUBLIC_BACKEND_URL: process.env.NEXT_PUBLIC_BACKEND_URL,
  },
};

module.exports = nextConfig;