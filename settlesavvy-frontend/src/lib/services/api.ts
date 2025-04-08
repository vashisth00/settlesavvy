/* eslint-disable @typescript-eslint/no-explicit-any */
// src/lib/services/api.js

import axios from 'axios';

// Create axios instance with base URL
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

// Create axios instance with baseURL
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to include auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Authentication service
export const authService = {
  // Login user
  login: async (credentials: any) => {
    const response = await api.post('/auth/login/', credentials);
    if (response.data.token) {
      localStorage.setItem('token', response.data.token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    return response;
  },

  // Register user
  register: async (userData: any) => {
    const response = await api.post('/auth/register/', userData);
    if (response.data.token) {
      localStorage.setItem('token', response.data.token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    return response;
  },

  // Logout user
  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  },

  // Get current user from local storage
  getCurrentUser: () => {
    const userStr = localStorage.getItem('user');
    if (userStr) {
      try {
        return JSON.parse(userStr);
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      } catch (error) {
        return null;
      }
    }
    return null;
  },

  // Check if user is authenticated
  isAuthenticated: () => {
    return !!localStorage.getItem('token');
  }
};

// Map service
export const mapService = {
  // Get all maps for current user
  getAllMaps: () => {
    return api.get('/maps/');
  },

  // Get single map by ID
  getMap: (mapId: any) => {
    return api.get(`/maps/${mapId}/`);
  },

  // Create new map
  createMap: (mapData: any) => {
    return api.post('/maps/', mapData);
  },

  // Update map
  updateMap: (mapId: any, mapData: any) => {
    return api.patch(`/maps/${mapId}/`, mapData);
  },

  // Delete map
  deleteMap: (mapId: any) => {
    return api.delete(`/maps/${mapId}/`);
  },

  // Get neighborhood scores for a map
  getMapScores: (mapId: any) => {
    return api.get(`/maps/${mapId}/scores/`);
  }
};

// Factor service
export const factorService = {
  // Get all factors
  getAllFactors: () => {
    return api.get('/factors/');
  },

  // Get map factors
  getMapFactors: (mapId: any) => {
    return api.get(`/map-factors/?map_id=${mapId}`);
  },

  // Add factor to map
  addFactorToMap: (factorData: any) => {
    return api.post('/map-factors/', factorData);
  },

  // Update map factor
  updateMapFactor: (mapFactorId: any, factorData: any) => {
    return api.patch(`/map-factors/${mapFactorId}/`, factorData);
  },

  // Remove factor from map
  removeFactorFromMap: (mapFactorId: any) => {
    return api.delete(`/map-factors/${mapFactorId}/`);
  }
};

export default api;