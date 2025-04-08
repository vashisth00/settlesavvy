'use client';

import { useEffect, useState } from 'react';
import dynamic from 'next/dynamic';
import 'leaflet/dist/leaflet.css';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Loader2 } from 'lucide-react';
import { mapService } from '@/lib/services/api';

// Dynamically import the map components to avoid SSR issues
const MapWithNoSSR = dynamic(
  () => import('./MapComponent'), 
  { 
    ssr: false,
    loading: () => (
      <div className='flex items-center justify-center h-[600px]'>
        <Loader2 className='h-12 w-12 animate-spin text-primary' />
      </div>
    )
  }
);

// Define interfaces
interface NeighborhoodData {
  geo_id: string;
  name: string;
  score: number;
  geometry: any;
  is_filtered: boolean;
}

interface MapVisualizationProps {
  mapId: string;
}

export default function MapVisualization({ mapId }: MapVisualizationProps) {
  const [map, setMap] = useState<any>(null);
  const [neighborhoods, setNeighborhoods] = useState<NeighborhoodData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  // Fetch map data
  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        
        // Get map details
        const mapResponse = await mapService.getMap(mapId);
        setMap(mapResponse.data);
        
        // Get neighborhood scores
        const scoresResponse = await mapService.getMapScores(mapId);
        setNeighborhoods(scoresResponse.data);
        
        setLoading(false);
      } catch (err) {
        setError('Failed to load map data. Please try again later.');
        setLoading(false);
        console.error('Error fetching map data:', err);
      }
    };
    
    if (mapId) {
      fetchData();
    }
  }, [mapId]);
  
  if (loading) {
    return (
      <div className='flex items-center justify-center h-64'>
        <Loader2 className='mr-2 h-16 w-16 animate-spin text-primary' />
        <span>Loading map data...</span>
      </div>
    );
  }
  
  if (error) {
    return <div className='p-4 text-red-500 font-medium'>{error}</div>;
  }
  
  if (!map) {
    return <div className='p-4 text-red-500 font-medium'>Map not found</div>;
  }
  
  return (
    <Card className='w-full'>
      <CardHeader>
        <CardTitle>{map.name}</CardTitle>
      </CardHeader>
      <CardContent>
        <div className='h-[600px] w-full relative'>
          <MapWithNoSSR map={map} neighborhoods={neighborhoods} />
        </div>
      </CardContent>
    </Card>
  );
}