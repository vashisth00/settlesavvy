// src/lib/services/api/map-service.ts

// Types
export interface MapData {
  map_id: string;
  name: string;
  created_stamp: string;
  last_updated: string;
  center_point: unknown;
  zoom_level: number;
}

export interface CreateMapData {
  name: string;
  latitude?: number;
  longitude?: number;
  zoom_level: number;
}

 export interface MapFactorData {
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

export interface NeighborhoodScoreData {
  geo_id: string;
  name: string;
  score: number;
  is_filtered: boolean;
  geometry: unknown;
}

// Map service