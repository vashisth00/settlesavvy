// src/lib/services/api/auth-service.ts
import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

// Types
interface LoginData {
  username: string;
  password: string;
}

interface RegisterData {
  username: string;
  email: string;
  password: string;
  first_name?: string;
  last_name?: string;
  phone?: string;
  is_realtor?: boolean;
  preferred_city?: string;
  preferred_state?: string;
}

interface AuthResponse {
  token: string;
  user: {
    id: number;
    username: string;
    email: string;
    first_name: string;
    last_name: string;
    is_realtor: boolean;
  };
}

// Auth service
const authService = {
  // Login user
  async login(loginData: LoginData): Promise<AuthResponse> {
    const response = await axios.post<AuthResponse>(`${API_URL}/auth/login/`, loginData);
    
    // Save auth data
    if (response.data.token) {
      localStorage.setItem('token', response.data.token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    
    return response.data;
  },
  
  // Register user
  async register(registerData: RegisterData): Promise<AuthResponse> {
    const response = await axios.post<AuthResponse>(`${API_URL}/auth/register/`, registerData);
    
    // Save auth data
    if (response.data.token) {
      localStorage.setItem('token', response.data.token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    
    return response.data;
  },
  
  // Logout user
  logout(): void {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  },
  
  // Get current user
  getCurrentUser(): unknown {
    const userStr = localStorage.getItem('user');
    if (userStr) {
      try {
        return JSON.parse(userStr);
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      } catch (e) {
        return null;
      }
    }
    return null;
  },
  
  // Get auth token
  getToken(): string | null {
    return localStorage.getItem('token');
  },
  
  // Check if user is authenticated
  isAuthenticated(): boolean {
    return !!this.getToken();
  }
};

export { authService };