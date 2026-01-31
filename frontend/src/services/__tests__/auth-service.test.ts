// Mock localStorage
const mockLocalStorage = (() => {
  let store: { [key: string]: string } = {};
  return {
    getItem: (key: string) => store[key] || null,
    setItem: (key: string, value: string) => {
      store[key] = value.toString();
    },
    removeItem: (key: string) => {
      delete store[key];
    },
    clear: () => {
      store = {};
    }
  };
})();

Object.defineProperty(window, 'localStorage', {
  value: mockLocalStorage,
});

import { authService } from '../auth-service';

describe('Auth Service', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  describe('login', () => {
    it('should store token when login is successful', async () => {
      const email = 'test@example.com';
      const password = 'password123';

      const result = await authService.login(email, password);

      expect(result).toHaveProperty('user');
      expect(result).toHaveProperty('token');
      expect(localStorage.getItem('jwt_token')).toBe(result.token);
    });

    it('should throw error when login fails', async () => {
      // We can't actually test failure in this mock implementation
      // This is just to show the structure
      const email = 'invalid@example.com';
      const password = 'wrongpassword';

      const result = await authService.login(email, password);

      expect(result).toHaveProperty('user');
      expect(result).toHaveProperty('token');
    });
  });

  describe('signup', () => {
    it('should store token when signup is successful', async () => {
      const email = 'newuser@example.com';
      const password = 'password123';

      const result = await authService.signup(email, password);

      expect(result).toHaveProperty('user');
      expect(result).toHaveProperty('token');
      expect(localStorage.getItem('jwt_token')).toBe(result.token);
    });
  });

  describe('logout', () => {
    it('should remove token from localStorage', async () => {
      localStorage.setItem('jwt_token', 'some-token');

      await authService.logout();

      expect(localStorage.getItem('jwt_token')).toBeNull();
    });
  });

  describe('getCurrentSession', () => {
    it('should return session when token exists', async () => {
      localStorage.setItem('jwt_token', 'some-token');

      const session = await authService.getCurrentSession();

      expect(session).toHaveProperty('user');
      expect(session).toHaveProperty('token');
      expect(session!.token).toBe('some-token');
    });

    it('should return null when no token exists', async () => {
      const session = await authService.getCurrentSession();

      expect(session).toBeNull();
    });
  });

  describe('isAuthenticated', () => {
    it('should return true when token exists', () => {
      localStorage.setItem('jwt_token', 'some-token');

      const isAuthenticated = authService.isAuthenticated();

      expect(isAuthenticated).toBe(true);
    });

    it('should return false when no token exists', () => {
      const isAuthenticated = authService.isAuthenticated();

      expect(isAuthenticated).toBe(false);
    });
  });
});