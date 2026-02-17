import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse, InternalAxiosRequestConfig } from 'axios';

// Create axios instance with base configuration
const apiClient: AxiosInstance = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000',
  timeout: 10000, // 10 seconds timeout
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to include JWT token in all requests
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.set('Authorization', `Bearer ${token}`);
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor to handle common error cases
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle specific error cases here
    if (error.response?.status === 401) {
      // Token might be expired, redirect to login
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Function to validate token by making a request to a protected endpoint
export const validateToken = async (): Promise<boolean> => {
  try {
    const token = localStorage.getItem('access_token');
    if (!token) {
      return false;
    }

    // We can make a simple request to a protected endpoint to validate the token
    // For now, let's just verify the token exists and hasn't expired by decoding it
    // Alternatively, we could make an API call to a user/me endpoint if available

    // Simple validation - check if token exists
    return !!token;
  } catch (error) {
    console.error('Error validating token:', error);
    return false;
  }
};

export default apiClient;

// API service functions for tasks
export const taskApi = {
  // Get all user tasks
  getTasks: async (status?: 'all' | 'pending' | 'completed', limit?: number, offset?: number) => {
    const params: any = {};
    if (status) params.status = status;
    if (limit) params.limit = limit;
    if (offset) params.offset = offset;

    const response: AxiosResponse = await apiClient.get('/api/tasks', { params });
    return response.data;
  },

  // Create a new task
  createTask: async (title: string, description?: string) => {
    const response: AxiosResponse = await apiClient.post('/api/tasks', {
      title,
      description: description || null
    });
    return response.data;
  },

  // Update a task
  updateTask: async (taskId: number, title?: string, description?: string, completed?: boolean) => {
    const response: AxiosResponse = await apiClient.put(`/api/tasks/${taskId}`, {
      title,
      description,
      completed
    });
    return response.data;
  },

  // Toggle task completion status
  toggleTaskCompletion: async (taskId: number) => {
    const response: AxiosResponse = await apiClient.patch(`/api/tasks/${taskId}/toggle-complete`);
    return response.data;
  },

  // Delete a task
  deleteTask: async (taskId: number) => {
    const response: AxiosResponse = await apiClient.delete(`/api/tasks/${taskId}`);
    return response.data;
  }
};

// API service functions for authentication
export const authApi = {
  // Register a new user
  register: async (email: string, name: string, password: string) => {
    const response: AxiosResponse = await apiClient.post('/api/auth/register', {
      email,
      name,
      password
    });
    return response.data;
  },

  // Login user
  login: async (email: string, password: string) => {
    const response: AxiosResponse = await apiClient.post('/api/auth/login', {
      email,
      password
    });

    // Store the token in localStorage as a backup measure
    if (response.data.access_token) {
      localStorage.setItem('access_token', response.data.access_token);
    }

    return response.data;
  },

  // Logout user
  logout: () => {
    localStorage.removeItem('access_token');
  },

  // Get current user info (if needed)
  getCurrentUser: async () => {
    try {
      const response: AxiosResponse = await apiClient.get('/api/auth/me'); // Using the new endpoint
      return response.data;
    } catch (error) {
      console.error('Error getting current user:', error);
      throw error;
    }
  }
};