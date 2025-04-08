'use client';

import { useEffect, useState } from 'react';
import { MapContainer, TileLayer, GeoJSON, useMap } from 'react-leaflet';
import L from 'leaflet';
import { Button } from '@/components/ui/button';

// Component to handle map center and zoom changes
function MapSetter({ center, zoom }: { center: [number, number]; zoom: number }) {
  const map = useMap();
  
  useEffect(() => {
    if (center && zoom) {
      map.setView(center, zoom);
    }
  }, [center, zoom, map]);
  
  return null;
}

// Define interfaces
interface NeighborhoodData {
  geo_id: string;
  name: string;
  score: number;
  geometry: any;
  is_filtered: boolean;
}

interface MapComponentProps {
  map: {
    center_point: any;
    zoom_level: number;
  };
  neighborhoods: NeighborhoodData[];
}

export default function MapComponent({ map, neighborhoods }: MapComponentProps) {
  const [legendVisible, setLegendVisible] = useState(true);
  
  // Fix Leaflet icons in Next.js
  useEffect(() => {
    // Only run on client-side
    delete L.Icon.Default.prototype._getIconUrl;
    L.Icon.Default.mergeOptions({
      iconRetinaUrl: '/images/marker-icon-2x.png',
      iconUrl: '/images/marker-icon.png',
      shadowUrl: '/images/marker-shadow.png',
    });
  }, []);
  
  // Function to style neighborhoods based on score
  const getNeighborhoodStyle = (feature: any) => {
    const neighborhood = neighborhoods.find(n => n.geo_id === feature.properties.geo_id);
    
    // Default style for neighborhoods without scores
    if (!neighborhood || neighborhood.is_filtered) {
      return {
        fillColor: '#cccccc',
        weight: 1,
        opacity: 0.7,
        color: '#666666',
        fillOpacity: 0.4
      };
    }
    
    // Color scale based on score (0-100)
    let fillColor = '#cccccc';
    const score = neighborhood.score;
    
    if (score >= 80) {
      fillColor = '#1a9850'; // Very high (dark green)
    } else if (score >= 60) {
      fillColor = '#91cf60'; // High (light green)
    } else if (score >= 40) {
      fillColor = '#ffffbf'; // Medium (yellow)
    } else if (score >= 20) {
      fillColor = '#fc8d59'; // Low (orange)
    } else {
      fillColor = '#d73027'; // Very low (red)
    }
    
    return {
      fillColor: fillColor,
      weight: 1,
      opacity: 0.7,
      color: '#666666',
      fillOpacity: 0.7
    };
  };
  
  // Handle neighborhood click
  const onEachNeighborhood = (feature: any, layer: L.Layer) => {
    const properties = feature.properties;
    
    // Add tooltip
    if (layer instanceof L.Path) {
      layer.bindTooltip(properties.name || 'Unnamed Area', {
        permanent: false,
        direction: 'center',
        className: 'neighborhood-tooltip'
      });
      
      // Add click handler
      layer.on({
        click: (e: L.LeafletMouseEvent) => {
          const neighborhood = neighborhoods.find(n => n.geo_id === feature.properties.geo_id);
          
          if (neighborhood) {
            const popupContent = `
              <div>
                <h4 class="font-bold">${feature.properties.name || 'Unnamed Area'}</h4>
                <p>Score: ${neighborhood.score ? neighborhood.score.toFixed(1) : 'N/A'}</p>
                ${neighborhood.is_filtered ? '<p class="font-bold text-red-500">Filtered out by preferences</p>' : ''}
              </div>
            `;
            
            const popup = L.popup()
              .setLatLng(e.latlng)
              .setContent(popupContent)
              .openOn(e.target._map);
          }
        }
      });
    }
  };
  
  const mapCenter = map.center_point ? 
    [map.center_point.coordinates[1], map.center_point.coordinates[0]] as [number, number] : 
    [37.8, -96.9] as [number, number]; // Default to US center
  
  const mapZoom = map.zoom_level || 10;
  
  return (
    <>
      <MapContainer 
        center={mapCenter} 
        zoom={mapZoom} 
        style={{ height: '100%', width: '100%' }}
        className='rounded-md z-0'
      >
        <MapSetter center={mapCenter} zoom={mapZoom} />
        
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
        />
        
        {/* Render neighborhoods */}
        {neighborhoods.length > 0 && (
          <GeoJSON
            key='neighborhoods'
            data={{
              type: 'FeatureCollection',
              features: neighborhoods.map(n => ({
                type: 'Feature',
                properties: {
                  geo_id: n.geo_id,
                  name: n.name,
                  score: n.score,
                  is_filtered: n.is_filtered
                },
                geometry: n.geometry
              }))
            }}
            style={getNeighborhoodStyle}
            onEachFeature={onEachNeighborhood}
          />
        )}
      </MapContainer>
      
      {/* Map Legend */}
      {legendVisible && (
        <div className='absolute bottom-5 right-5 bg-white p-3 shadow-md rounded-md z-10 w-48'>
          <h4 className='text-sm font-bold mb-2'>Neighborhood Score</h4>
          <div className='flex items-center mb-1'>
            <div className='w-4 h-4 bg-[#1a9850] mr-2'></div>
            <span className='text-xs'>80-100 (Very High)</span>
          </div>
          <div className='flex items-center mb-1'>
            <div className='w-4 h-4 bg-[#91cf60] mr-2'></div>
            <span className='text-xs'>60-79 (High)</span>
          </div>
          <div className='flex items-center mb-1'>
            <div className='w-4 h-4 bg-[#ffffbf] mr-2'></div>
            <span className='text-xs'>40-59 (Medium)</span>
          </div>
          <div className='flex items-center mb-1'>
            <div className='w-4 h-4 bg-[#fc8d59] mr-2'></div>
            <span className='text-xs'>20-39 (Low)</span>
          </div>
          <div className='flex items-center mb-1'>
            <div className='w-4 h-4 bg-[#d73027] mr-2'></div>
            <span className='text-xs'>0-19 (Very Low)</span>
          </div>
          <div className='flex items-center mb-2'>
            <div className='w-4 h-4 bg-[#cccccc] mr-2'></div>
            <span className='text-xs'>No Data or Filtered</span>
          </div>
          <Button 
            variant='outline' 
            size='sm' 
            className='w-full text-xs'
            onClick={() => setLegendVisible(false)}
          >
            Close
          </Button>
        </div>
      )}
      
      {!legendVisible && (
        <Button 
          variant='outline' 
          className='absolute bottom-5 right-5 z-10'
          onClick={() => setLegendVisible(true)}
        >
          Show Legend
        </Button>
      )}
    </>
  );
}