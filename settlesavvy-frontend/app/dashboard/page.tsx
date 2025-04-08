'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { authService, mapService } from '@/lib/services/api';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Loader2, Plus, Map, Settings, User } from 'lucide-react';
import { toast } from 'sonner';

interface MapData {
  map_id: string;
  name: string;
  created_stamp: string;
  last_updated: string;
}

export default function DashboardPage() {
  const [user, setUser] = useState<any>(null);
  const [maps, setMaps] = useState<MapData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  useEffect(() => {
    // Check if user is logged in
    const currentUser = authService.getCurrentUser();
    if (!currentUser) {
      toast.error('Authentication required', {
        description: 'Please log in to access the dashboard'
      });
      router.push('/auth/login');
      return;
    }
    
    setUser(currentUser);
    
    // Fetch user's maps
    const fetchMaps = async () => {
      try {
        const response = await mapService.getAllMaps();
        setMaps(response.data);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching maps:', err);
        setError('Failed to load your maps. Please try again later.');
        setLoading(false);
      }
    };
    
    fetchMaps();
  }, [router]);

  const handleLogout = () => {
    authService.logout();
    toast.success('Logged out successfully');
    router.push('/');
  };

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm">
        <div className="container mx-auto flex h-16 items-center justify-between px-4">
          <Link href="/" className="text-2xl font-bold text-primary">
            Settle Savvy
          </Link>
          <div className="flex items-center gap-4">
            <Button variant="ghost" size="sm">
              <User className="mr-2 h-4 w-4" />
              {user?.username || 'Profile'}
            </Button>
            <Button variant="ghost" size="sm" onClick={handleLogout}>
              Sign Out
            </Button>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        <div className="mb-8 flex items-center justify-between">
          <h1 className="text-3xl font-bold">Your Dashboard</h1>
          <Button asChild>
            <Link href="/maps/new">
              <Plus className="mr-2 h-4 w-4" />
              Create New Map
            </Link>
          </Button>
        </div>

        {error && (
          <div className="mb-8 rounded-md bg-red-50 p-4 text-red-600">
            {error}
          </div>
        )}

        <div className="mb-8">
          <h2 className="mb-4 text-xl font-semibold">Your Maps</h2>
          
          {maps.length === 0 ? (
            <Card className="text-center p-8">
              <CardContent className="pt-6">
                <Map className="mx-auto h-12 w-12 text-gray-400" />
                <p className="mt-4 text-gray-500">You haven't created any maps yet.</p>
              </CardContent>
              <CardFooter className="justify-center">
                <Button asChild>
                  <Link href="/maps/new">
                    <Plus className="mr-2 h-4 w-4" />
                    Create Your First Map
                  </Link>
                </Button>
              </CardFooter>
            </Card>
          ) : (
            <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
              {maps.map((map) => (
                <Card key={map.map_id}>
                  <CardHeader>
                    <CardTitle>{map.name}</CardTitle>
                    <CardDescription>
                      Created: {new Date(map.created_stamp).toLocaleDateString()}
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-gray-500">
                      Last updated: {new Date(map.last_updated).toLocaleDateString()}
                    </p>
                  </CardContent>
                  <CardFooter className="flex justify-between">
                    <Button variant="outline" size="sm" asChild>
                      <Link href={`/maps/${map.map_id}/edit`}>
                        <Settings className="mr-2 h-4 w-4" />
                        Edit
                      </Link>
                    </Button>
                    <Button size="sm" asChild>
                      <Link href={`/maps/${map.map_id}`}>
                        <Map className="mr-2 h-4 w-4" />
                        View
                      </Link>
                    </Button>
                  </CardFooter>
                </Card>
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  );
}