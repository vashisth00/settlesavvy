'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { ArrowLeft, Loader2, Save } from 'lucide-react';
import { toast } from 'sonner';

import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { authService, mapService } from '@/lib/services/api';

export default function MapEditPage({ params }: { params: { id: string } }) {
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [map, setMap] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [formData, setFormData] = useState({
    name: '',
    latitude: '',
    longitude: '',
    zoom_level: ''
  });
  
  const router = useRouter();
  const mapId = params.id;
  
  useEffect(() => {
    // Check if user is logged in
    if (!authService.isAuthenticated()) {
      toast.error('Authentication required', {
        description: 'Please log in to edit this map'
      });
      router.push('/auth/login');
      return;
    }
    
    // Fetch map data
    const fetchMap = async () => {
      try {
        const response = await mapService.getMap(mapId);
        const mapData = response.data;
        
        setMap(mapData);
        
        // Extract latitude and longitude from center_point
        let latitude = '';
        let longitude = '';
        
        if (mapData.center_point && mapData.center_point.coordinates) {
          // GeoJSON format is [longitude, latitude]
          longitude = mapData.center_point.coordinates[0].toString();
          latitude = mapData.center_point.coordinates[1].toString();
        }
        
        setFormData({
          name: mapData.name || '',
          latitude,
          longitude,
          zoom_level: mapData.zoom_level?.toString() || '10'
        });
        
        setLoading(false);
      } catch (err) {
        console.error('Error fetching map:', err);
        setError('Failed to load map. It may not exist or you may not have permission to edit it.');
        setLoading(false);
      }
    };
    
    fetchMap();
  }, [mapId, router]);
  
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    
    try {
      // Convert string values to numbers where needed
      const updateData = {
        name: formData.name,
        latitude: formData.latitude ? parseFloat(formData.latitude) : undefined,
        longitude: formData.longitude ? parseFloat(formData.longitude) : undefined,
        zoom_level: formData.zoom_level ? parseFloat(formData.zoom_level) : undefined
      };
      
      // Remove undefined values
      Object.keys(updateData).forEach(key => {
        if (updateData[key as keyof typeof updateData] === undefined) {
          delete updateData[key as keyof typeof updateData];
        }
      });
      
      // Update the map
      await mapService.updateMap(mapId, updateData);
      
      toast.success('Map updated successfully');
      
      // Navigate back to the map view
      router.push(`/maps/${mapId}`);
    } catch (err: any) {
      console.error('Error updating map:', err);
      
      toast.error('Failed to update map', {
        description: err.response?.data?.detail || 'An error occurred while updating the map.'
      });
    } finally {
      setSaving(false);
    }
  };
  
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
            <Link href={`/maps/${mapId}`}>
              <ArrowLeft className="mr-2 h-4 w-4" />
              Back to Map
            </Link>
          </Button>
        </div>
        
        <div className="mb-6">
          <h1 className="text-3xl font-bold">Edit Map: {map?.name}</h1>
          <p className="mt-1 text-gray-600">
            Update the details of your map
          </p>
        </div>
        
        <Card className="w-full max-w-2xl mx-auto">
          <CardHeader>
            <CardTitle>Edit Map Settings</CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="space-y-2">
                <Label htmlFor="name">Map Name</Label>
                <Input
                  id="name"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  placeholder="My Neighborhood Map"
                  required
                />
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="latitude">Latitude</Label>
                  <Input
                    id="latitude"
                    name="latitude"
                    type="number"
                    step="any"
                    value={formData.latitude}
                    onChange={handleChange}
                    placeholder="e.g., 37.7749"
                  />
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor="longitude">Longitude</Label>
                  <Input
                    id="longitude"
                    name="longitude"
                    type="number"
                    step="any"
                    value={formData.longitude}
                    onChange={handleChange}
                    placeholder="e.g., -122.4194"
                  />
                </div>
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="zoom_level">Zoom Level (1-18)</Label>
                <Input
                  id="zoom_level"
                  name="zoom_level"
                  type="number"
                  min="1"
                  max="18"
                  step="any"
                  value={formData.zoom_level}
                  onChange={handleChange}
                  placeholder="10"
                />
                <p className="text-sm text-gray-500">
                  Higher values zoom in closer
                </p>
              </div>
              
              <div className="flex justify-end gap-4">
                <Button type="button" variant="outline" asChild>
                  <Link href={`/maps/${mapId}`}>Cancel</Link>
                </Button>
                
                <Button type="submit" disabled={saving}>
                  {saving ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Saving...
                    </>
                  ) : (
                    <>
                      <Save className="mr-2 h-4 w-4" />
                      Save Changes
                    </>
                  )}
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}