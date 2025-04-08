import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { mapService } from '@/lib/services/api';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Slider } from '@/components/ui/slider';
import { Loader2, Map } from 'lucide-react';
import { toast } from 'sonner';

const CreateMapForm = () => {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    latitude: 0,
    longitude: 0,
    zoom_level: 11
  });

  const handleInputChange = (e: { target: { name: any; value: any; }; }) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleZoomChange = (value: any[]) => {
    setFormData({
      ...formData,
      zoom_level: value[0]
    });
  };

  const handleSubmit = async (e: { preventDefault: () => void; }) => {
    e.preventDefault();
    setLoading(true);

    try {
      // Ensure latitude and longitude are numbers
      const mapData = {
        ...formData,
        latitude: parseFloat(formData.latitude),
        longitude: parseFloat(formData.longitude),
        zoom_level: parseFloat(formData.zoom_level)
      };

      const response = await mapService.createMap(mapData);
      toast.success('Map created successfully!');
      
      // Redirect to the dashboard
      router.push('/dashboard');
    } catch (error) {
      console.error('Error creating map:', error);
      const errorMessage = error.response?.data?.detail || 
                           'Failed to create map. Please try again.';
      toast.error('Error creating map', {
        description: errorMessage
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader>
        <CardTitle className="text-2xl text-center">Create New Map</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="name">Map Name</Label>
            <Input
              id="name"
              name="name"
              value={formData.name}
              onChange={handleInputChange}
              placeholder="Enter map name"
              required
            />
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="latitude">Latitude</Label>
            <Input
              id="latitude"
              name="latitude"
              type="number"
              step="any"
              value={formData.latitude}
              onChange={handleInputChange}
              placeholder="Enter latitude"
              required
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
              onChange={handleInputChange}
              placeholder="Enter longitude"
              required
            />
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="zoom_level">Zoom Level: {formData.zoom_level}</Label>
            <Slider
              id="zoom_level"
              min={1}
              max={20}
              step={0.1}
              value={[formData.zoom_level]}
              onValueChange={handleZoomChange}
            />
          </div>
          
          <Button type="submit" className="w-full" disabled={loading}>
            {loading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Creating...
              </>
            ) : (
              <>
                <Map className="mr-2 h-4 w-4" />
                Create Map
              </>
            )}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
};

export default CreateMapForm;