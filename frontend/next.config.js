/** @type {import('next').NextConfig} */
const nextConfig = {
  // Disable static export - we're running on Hugging Face Spaces, not GitHub Pages
  // output: 'export',

  // No basePath needed for Hugging Face Spaces
  // basePath: isProd ? `/${repoName}` : '',

  // Disable image optimization for compatibility
  images: {
    unoptimized: true,
  },

  // No trailing slashes needed
  trailingSlash: false,

  // Environment variables
  env: {
    NEXT_PUBLIC_API_BASE_URL: process.env.NEXT_PUBLIC_API_BASE_URL,
    NEXT_PUBLIC_BACKEND_URL: process.env.NEXT_PUBLIC_BACKEND_URL,
  },
};

module.exports = nextConfig;