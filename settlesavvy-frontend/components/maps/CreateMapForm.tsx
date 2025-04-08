'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { toast } from 'sonner';

import { Button } from '@/components/ui/button';
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Loader2 } from 'lucide-react';
import { mapService } from '@/lib/services/api';

// Form schema
const formSchema = z.object({
  name: z.string().min(3, 'Map name must be at least 3 characters'),
  latitude: z.coerce.number().optional(),
  longitude: z.coerce.number().optional(),
  zoom_level: z.coerce.number().min(1).max(18).default(10),
});

export default function CreateMapForm() {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const router = useRouter();
  
  // Initialize form
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      name: '',
      zoom_level: 10,
    },
  });
  
  async function onSubmit(values: z.infer<typeof formSchema>) {
    try {
      setIsSubmitting(true);
      
      // Submit the map data to API
      const response = await mapService.createMap({
        name: values.name,
        latitude: values.latitude,
        longitude: values.longitude,
        zoom_level: values.zoom_level,
      });
      
      toast.success('Map created successfully');
      
      // Redirect to the new map page
      router.push(`/dashboard`);
      
    } catch (error: any) {
      console.error('Error creating map:', error);
      toast.error('Failed to create map', {
        description: error.response?.data?.message || 'An unexpected error occurred',
      });
    } finally {
      setIsSubmitting(false);
    }
  }
  
  return (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader>
        <CardTitle>Create New Map</CardTitle>
        <CardDescription>
          Create a map to visualize neighborhood data based on your preferences.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
            <FormField
              control={form.control}
              name="name"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Map Name</FormLabel>
                  <FormControl>
                    <Input placeholder="My Neighborhood Map" {...field} />
                  </FormControl>
                  <FormDescription>
                    Give your map a meaningful name so you can find it later.
                  </FormDescription>
                  <FormMessage />
                </FormItem>
              )}
            />
            
            <div className="grid grid-cols-2 gap-4">
              <FormField
                control={form.control}
                name="latitude"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Latitude (optional)</FormLabel>
                    <FormControl>
                      <Input type="number" step="any" placeholder="37.7749" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              
              <FormField
                control={form.control}
                name="longitude"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Longitude (optional)</FormLabel>
                    <FormControl>
                      <Input type="number" step="any" placeholder="-122.4194" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>
            
            <FormField
              control={form.control}
              name="zoom_level"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Zoom Level</FormLabel>
                  <FormControl>
                    <Input type="number" min={1} max={18} {...field} />
                  </FormControl>
                  <FormDescription>
                    Initial zoom level (1-18). Higher values zoom in closer.
                  </FormDescription>
                  <FormMessage />
                </FormItem>
              )}
            />
            
            <Button type="submit" className="w-full" disabled={isSubmitting}>
              {isSubmitting ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Creating...
                </>
              ) : (
                'Create Map'
              )}
            </Button>
          </form>
        </Form>
      </CardContent>
    </Card>
  );
}