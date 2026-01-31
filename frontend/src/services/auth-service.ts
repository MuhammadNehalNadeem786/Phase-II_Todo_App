import axios from 'axios';

const AUTH_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

const USER_KEY = 'auth_user';
const TOKEN_KEY = 'jwt_token';

export const authService = {
  login: async (email: string, password: string) => {
    try {
      const response = await axios.post(
        `${AUTH_BASE_URL}/auth/login`,
        { email, password },
        {
          headers: { 'Content-Type': 'application/json' }
        }
      );

      const { user, token } = response.data;

      localStorage.setItem(TOKEN_KEY, token);
      localStorage.setItem(USER_KEY, JSON.stringify(user));

      return { user, token };
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new Error(error.response?.data?.message || 'Login failed');
      }
      throw error;
    }
  },

  signup: async (email: string, password: string, username: string) => {
    try {
      const response = await axios.post(
        `${AUTH_BASE_URL}/auth/signup`,
        { username, email, password },
        {
          headers: { 'Content-Type': 'application/json' }
        }
      );

      const { user, token } = response.data;

      localStorage.setItem(TOKEN_KEY, token);
      localStorage.setItem(USER_KEY, JSON.stringify(user));

      return { user, token };
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new Error(error.response?.data?.message || 'Signup failed');
      }
      throw error;
    }
  },

  logout: async () => {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
    return { message: 'Successfully logged out' };
  },

  getCurrentSession: async () => {
    const token = localStorage.getItem(TOKEN_KEY);
    const user = localStorage.getItem(USER_KEY);

    if (!token || !user) return null;

    try {
      return {
        token,
        user: JSON.parse(user)
      };
    } catch {
      localStorage.removeItem(TOKEN_KEY);
      localStorage.removeItem(USER_KEY);
      return null;
    }
  },

  isAuthenticated: (): boolean => {
    return !!localStorage.getItem(TOKEN_KEY);
  }
};
