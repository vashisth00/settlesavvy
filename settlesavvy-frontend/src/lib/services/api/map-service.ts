// src/lib/services/api/map-service.ts
import { apiClient } from '../api';

// Types
interface MapData {
  map_id: string;
  name: string;
  created_stamp: string;
  last_updated: string;
  center_point: unknown;
  zoom_level: number;
}

interface CreateMapData {
  name: string;
  latitude?: number;
  longitude?: number;
  zoom_level: number;
}

interface MapFactorData {
  map_factor_id: string;
  map: string;
  factor: number;
  factor_name: string;
  weight: number;
  scoring_strategy: string;
  filter_strategy: string;
  score_tipping_1: number | null;
  score_tipping_2: number | null;
  filter_tipping_1: number | null;
  filter_tipping_2: number | null;
}

interface NeighborhoodScoreData {
  geo_id: string;
  name: string;
  score: number;
  is_filtered: boolean;
  geometry: unknown;
}

// Map service
const mapService = {
  // Get all maps
  getAllMaps() {
    return apiClient.get<MapData[]>('/maps/');
  },
  
  // Get a specific map
  getMap(mapId: string) {
    return apiClient.get<MapData>(`/maps/${mapId}/`);
  },
  
  // Create a new map
  createMap(mapData: CreateMapData) {
    return apiClient.post<MapData>('/maps/', mapData);
  },
  
  // Update a map
  updateMap(mapId: string, mapData: Partial<CreateMapData>) {
    return apiClient.patch<MapData>(`/maps/${mapId}/`, mapData);
  },
  
  // Delete a map
  deleteMap(mapId: string) {
    return apiClient.delete(`/maps/${mapId}/`);
  },
  
  // Get neighborhood scores for a map
  getMapScores(mapId: string) {
    return apiClient.get<NeighborhoodScoreData[]>(`/maps/${mapId}/scores/`);
  },
  
  // Get factors for a map
  getMapFactors(mapId: string) {
    return apiClient.get<MapFactorData[]>('/map-factors/', {
      params: { map_id: mapId }
    });
  },
  
  // Add a factor to a map
  addFactorToMap(mapId: string, factorData: Omit<MapFactorData, 'map_factor_id' | 'map' | 'factor_name'>) {
    return apiClient.post<MapFactorData>('/map-factors/', {
      ...factorData,
      map: mapId
    });
  },
  
  // Update a map factor
  updateMapFactor(mapFactorId: string, data: Partial<MapFactorData>) {
    return apiClient.patch<MapFactorData>(`/map-factors/${mapFactorId}/`, data);
  },
  
  // Delete a map factor
  deleteMapFactor(mapFactorId: string) {
    return apiClient.delete(`/map-factors/${mapFactorId}/`);
  },
  
  // Get all available factors
  getFactors() {
    return apiClient.get('/factors/');
  }
};

export { mapService };