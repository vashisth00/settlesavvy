'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { ArrowLeft } from 'lucide-react';
import { toast } from 'sonner';

import { Button } from '@/components/ui/button';
import { authService } from '@/lib/services/api';
import CreateMapForm from '../../../components/maps/CreateMapForm';

export default function CreateMapPage() {
  const router = useRouter();
  
  useEffect(() => {
    // Check if user is logged in
    if (!authService.isAuthenticated()) {
      toast.error('Authentication required', {
        description: 'Please log in to create a new map'
      });
      router.push('/auth/login');
    }
  }, [router]);
  
  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4">
        <div className="mb-6">
          <Button variant="ghost" size="sm" asChild>
            <Link href="/dashboard">
              <ArrowLeft className="mr-2 h-4 w-4" />
              Back to Dashboard
            </Link>
          </Button>
        </div>
        
        <div className="mb-8 text-center">
          <h1 className="text-3xl font-bold">Create a New Map</h1>
          <p className="mt-2 text-gray-600">
            Set up your map to start analyzing neighborhoods based on your preferences.
          </p>
        </div>
        
        <CreateMapForm />
      </div>
    </div>
  );
}