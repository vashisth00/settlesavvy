/* eslint-disable @typescript-eslint/no-explicit-any */
// lib/services/api.ts

import axios from "axios";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/";

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor to add auth token
apiClient.interceptors.request.use(
  (config) => {
    // Check if we are in a browser environment
    if (typeof window !== "undefined") {
      const token = localStorage.getItem("token");
      if (token) {
        config.headers.Authorization = `Token ${token}`;
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Authentication services
export const authService = {
  login: async (username: string, password: string) => {
    const response = await apiClient.post("auth/login/", { username, password });
    if (response.data.token) {
      localStorage.setItem("token", response.data.token);
      localStorage.setItem("user", JSON.stringify(response.data.user));
    }
    return response.data;
  },
  logout: () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
  },
  register: async (userData: any) => {
    return apiClient.post("auth/register/", userData);
  },
  getCurrentUser: () => {
    if (typeof window !== "undefined") {
      const user = localStorage.getItem("user");
      return user ? JSON.parse(user) : null;
    }
    return null;
  },
};

// Maps services
export const mapService = {
  getAllMaps: () => apiClient.get("maps/"),
  getMap: (id: string) => apiClient.get(`maps/${id}/`),
  createMap: (mapData: any) => apiClient.post("maps/", mapData),
  updateMap: (id: string, mapData: any) => apiClient.put(`maps/${id}/`, mapData),
  deleteMap: (id: string) => apiClient.delete(`maps/${id}/`),
  getMapScores: (id: string) => apiClient.get(`maps/${id}/factor_scores/`),
};

// Geography services
export const geoService = {
  getAllGeographies: () => apiClient.get("geographies/"),
  getGeography: (id: string) => apiClient.get(`geographies/${id}/`),
  getGeographiesByLocation: (lat: number, lng: number) => 
    apiClient.get(`geographies/by_location/?lat=${lat}&lng=${lng}`),
};

// Factors services
export const factorService = {
  getAllFactors: () => apiClient.get("factors/"),
  getFactor: (id: number) => apiClient.get(`factors/${id}/`),
  getFactorsByCategory: (category: string) => apiClient.get(`factors/?category=${category}`),
};

// Map-Factor services
export const mapFactorService = {
  getMapFactors: (mapId: string) => apiClient.get(`map-factors/?map=${mapId}`),
  createMapFactor: (mapFactorData: any) => apiClient.post("map-factors/", mapFactorData),
  updateMapFactor: (id: string, mapFactorData: any) => apiClient.put(`map-factors/${id}/`, mapFactorData),
  deleteMapFactor: (id: string) => apiClient.delete(`map-factors/${id}/`),
  calculateScores: (id: string) => apiClient.post(`map-factors/${id}/calculate_scores/`),
};

// Points of Interest services
export const poiService = {
  getMapPOIs: (mapId: string) => apiClient.get(`points-of-interest/?map=${mapId}`),
  createPOI: (poiData: any) => apiClient.post("points-of-interest/", poiData),
  updatePOI: (id: string, poiData: any) => apiClient.put(`points-of-interest/${id}/`, poiData),
  deletePOI: (id: string) => apiClient.delete(`points-of-interest/${id}/`),
};

export default apiClient;