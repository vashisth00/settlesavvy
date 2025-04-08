'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { ArrowLeft, Loader2, Settings } from 'lucide-react';
import { toast } from 'sonner';

import { Button } from '@/components/ui/button';
import { authService, mapService } from '@/lib/services/api';
import MapVisualization from '../../../components/maps/MapVisualization';

export default function MapDetailPage({ params }: { params: { id: string } }) {
  const [loading, setLoading] = useState(true);
  const [map, setMap] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();
  const mapId = params.id;
  
  useEffect(() => {
    // Check if user is logged in
    if (!authService.isAuthenticated()) {
      toast.error('Authentication required', {
        description: 'Please log in to view this map'
      });
      router.push('/auth/login');
      return;
    }
    
    // Fetch map data
    const fetchMap = async () => {
      try {
        const response = await mapService.getMap(mapId);
        setMap(response.data);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching map:', err);
        setError('Failed to load map. It may not exist or you may not have permission to view it.');
        setLoading(false);
      }
    };
    
    fetchMap();
  }, [mapId, router]);
  
  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }
  
  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 p-8">
        <div className="container mx-auto">
          <div className="mb-6">
            <Button variant="ghost" size="sm" asChild>
              <Link href="/dashboard">
                <ArrowLeft className="mr-2 h-4 w-4" />
                Back to Dashboard
              </Link>
            </Button>
          </div>
          
          <div className="rounded-lg bg-red-50 p-6 text-center">
            <h1 className="text-2xl font-bold text-red-600">Error</h1>
            <p className="mt-2 text-red-600">{error}</p>
            <Button className="mt-4" asChild>
              <Link href="/dashboard">Go to Dashboard</Link>
            </Button>
          </div>
        </div>
      </div>
    );
  }
  
  return (
    <div className="min-h-screen bg-gray-50 py-6">
      <div className="container mx-auto px-4">
        <div className="mb-6 flex items-center justify-between">
          <Button variant="ghost" size="sm" asChild>
            <Link href="/dashboard">
              <ArrowLeft className="mr-2 h-4 w-4" />
              Back to Dashboard
            </Link>
          </Button>
          
          <Button variant="outline" size="sm" asChild>
            <Link href={`/maps/${mapId}/edit`}>
              <Settings className="mr-2 h-4 w-4" />
              Edit Map
            </Link>
          </Button>
        </div>
        
        <div className="mb-6">
          <h1 className="text-3xl font-bold">{map?.name || 'Map Details'}</h1>
          <p className="mt-1 text-gray-600">
            Created: {map?.created_stamp ? new Date(map.created_stamp).toLocaleString() : 'Unknown date'}
          </p>
        </div>
        
        <MapVisualization mapId={mapId} />
      </div>
    </div>
  );
}