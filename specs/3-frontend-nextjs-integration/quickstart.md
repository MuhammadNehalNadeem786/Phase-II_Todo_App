# Quickstart: Frontend Application & Full-Stack Integration (Next.js)

## Prerequisites

- Node.js 18+
- npm or yarn package manager
- Access to the backend API (running on http://localhost:8000 by default)
- Better Auth configured for the frontend

## Project Setup

### 1. Initialize Next.js Project
```bash
npx create-next-app@latest frontend
cd frontend
```

### 2. Install Dependencies
```bash
npm install axios react-icons better-auth
# Or if using yarn
yarn add axios react-icons better-auth
```

### 3. Install Development Dependencies
```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

## Environment Configuration

### 1. Create .env.local file
```bash
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000
```

### 2. Configure Next.js for Environment Variables
```javascript
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
}

module.exports = nextConfig
```

## API Client Setup

### 1. Create API Client Service
```javascript
// src/services/api-client.js
import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: `${API_BASE_URL}/signup`,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add JWT token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('jwt_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle 401/403 errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401 || error.response?.status === 403) {
      // Redirect to login page
      localStorage.removeItem('jwt_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default apiClient;
```

## Authentication Setup

### 1. Better Auth Integration
```javascript
// src/services/auth-service.js
import { signIn, signOut, getSession } from 'better-auth/react';

export const authService = {
  // Login function
  login: async (email, password) => {
    try {
      const response = await signIn('credentials', {
        email,
        password,
        redirect: false,
      });
      return response;
    } catch (error) {
      throw error;
    }
  },

  // Signup function
  signup: async (email, password) => {
    try {
      const response = await signIn('email-password', {
        email,
        password,
        redirect: false,
      });
      return response;
    } catch (error) {
      throw error;
    }
  },

  // Logout function
  logout: async () => {
    try {
      await signOut({ redirect: false });
      localStorage.removeItem('jwt_token');
    } catch (error) {
      throw error;
    }
  },

  // Get current session
  getCurrentSession: async () => {
    try {
      const session = await getSession();
      return session;
    } catch (error) {
      return null;
    }
  },
};
```

## Frontend Routing Setup

### 1. Create Protected Route Component
```javascript
// src/components/common/ProtectedRoute.js
'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { authService } from '@/services/auth-service';

export default function ProtectedRoute({ children }) {
  const [isAuthenticated, setIsAuthenticated] = useState(null);
  const router = useRouter();

  useEffect(() => {
    const checkAuth = async () => {
      const session = await authService.getCurrentSession();
      if (!session) {
        router.push('/login');
      } else {
        setIsAuthenticated(true);
      }
    };

    checkAuth();
  }, [router]);

  if (isAuthenticated === null) {
    return <div>Loading...</div>; // Loading state
  }

  return isAuthenticated ? children : null;
}
```

### 2. App Router Layout Structure
```
src/app/
├── layout.js          # Root layout
├── page.js            # Home page (redirects to login/dashboard)
├── (auth)/            # Authentication routes
│   ├── login/page.js
│   ├── signup/page.js
│   └── layout.js
└── dashboard/         # Protected routes
    ├── page.js
    └── layout.js
```

## Task Management Components

### 1. Task List Component
```javascript
// src/components/tasks/TaskList.js
'use client';

import { useState, useEffect } from 'react';
import TaskItem from './TaskItem';
import { getTasks } from '@/services/task-service';

export default function TaskList({ userId }) {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const data = await getTasks(userId);
        setTasks(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    if (userId) {
      fetchTasks();
    }
  }, [userId]);

  if (loading) return <div>Loading tasks...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="space-y-4">
      {tasks.map((task) => (
        <TaskItem key={task.id} task={task} />
      ))}
    </div>
  );
}
```

## Running the Application

### 1. Development Mode
```bash
cd frontend
npm run dev
# App will run on http://localhost:3000
```

### 2. Production Build
```bash
npm run build
npm start
```

## API Integration Testing

### 1. Test Authentication Flow
1. Navigate to `/login` or `/signup`
2. Submit valid credentials
3. Verify JWT token is stored and API requests include Authorization header

### 2. Test Task Management
1. Ensure authenticated user session
2. Create, read, update, delete tasks
3. Verify all operations work with proper authentication headers
4. Test error handling for unauthorized access

## Common Issues and Solutions

### JWT Token Not Being Sent
- Verify token is stored in localStorage after login
- Check that API client interceptor is properly configured
- Ensure Authorization header format is `Bearer <token>`

### 401/403 Errors Not Handled
- Verify response interceptor is properly configured
- Check that logout function clears token from storage
- Ensure redirect to login page happens after auth errors

### Route Protection Not Working
- Verify ProtectedRoute component is wrapping protected content
- Check that session validation is working correctly
- Ensure unauthorized users are redirected to login

## Deployment Notes

### Environment Variables
- Ensure NEXT_PUBLIC_API_BASE_URL points to the correct backend URL
- Set up proper CORS configuration between frontend and backend
- Use HTTPS in production for all API communications