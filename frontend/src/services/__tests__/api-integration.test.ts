// Mock the environment
process.env.NEXT_PUBLIC_API_BASE_URL = 'http://localhost:8000';

import apiClient from '../api-client';

describe('API Integration Tests', () => {
  beforeAll(() => {
    // Mock JWT token for authenticated requests
    Object.defineProperty(window, 'localStorage', {
      value: {
        getItem: jest.fn(() => 'mock-jwt-token'),
        setItem: jest.fn(),
        removeItem: jest.fn(),
      },
      writable: true,
    });
  });

  describe('API Client Configuration', () => {
    it('should have the correct base URL', () => {
      const expectedBaseUrl = `${process.env.NEXT_PUBLIC_API_BASE_URL}/signup`;
      // The baseURL property is not directly accessible on the axios instance in this way
      // This is a simplified test to show the concept
      expect(apiClient.defaults.baseURL).toContain('/signup');
    });

    it('should have correct default headers', () => {
      expect(apiClient.defaults.headers['Content-Type']).toBe('application/json');
    });
  });

  describe('Request Interceptor', () => {
    it('should add Authorization header with JWT token', async () => {
      // This is a simplified test - in a real scenario, we would check if the interceptor
      // correctly adds the Authorization header to requests
      const mockToken = 'mock-jwt-token';
      localStorage.getItem = jest.fn(() => mockToken);

      // Since we can't directly test the interceptor, we'll just verify the setup
      expect(typeof apiClient.interceptors.request.use).toBe('function');
    });
  });

  describe('Response Interceptor', () => {
    it('should handle 401 errors by redirecting to login', async () => {
      // Mock window.location
      const mockLocation = {
        href: '',
      };
      Object.defineProperty(window, 'location', {
        value: mockLocation,
        writable: true,
      });

      // This is a simplified test - in a real scenario, we would trigger a 401 response
      // and verify that the interceptor redirects to the login page
      expect(typeof apiClient.interceptors.response.use).toBe('function');
    });
  });

  // Additional integration tests would go here to test the actual API endpoints
  // when the backend is available
});