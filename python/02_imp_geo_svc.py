
## Implementing Geocoding Services:
class SimpleGeocoder:
    """Simple geocoding service using free APIs"""
    
    def __init__(self):
        # Using OpenStreetMap Nominatim (free geocoding service)
        self.base_url = "https://nominatim.openstreetmap.org/search"
        self.headers = {
            'User-Agent': 'WeatherApp/1.0 (Educational Project)'  # Required by Nominatim
        }
    
    def geocode_location(self, location_name):
        """
        Convert location name to coordinates using geocoding
        
        Args:
            location_name: String name of location (e.g., "New York, NY")
            
        Returns:
            dict with latitude, longitude, and display name, or None if not found
        """
        try:
            # Prepare API request
            params = {
                'q': location_name,
                'format': 'json',
                'limit': 1,  # Only get the best match
                'addressdetails': 1
            }
            
            print(f"Searching for location: {location_name}")
            
            # Make API request
            response = requests.get(
                self.base_url, 
                params=params, 
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                results = response.json()
                
                if results:
                    # Extract the best result
                    best_result = results[0]
                    
                    location_data = {
                        'latitude': float(best_result['lat']),
                        'longitude': float(best_result['lon']),
                        'display_name': best_result['display_name'],
                        'type': best_result.get('type', 'location'),
                        'importance': float(best_result.get('importance', 0))
                    }
                    
                    print(f"✓ Found: {location_data['display_name']}")
                    return location_data
                else:
                    print(f"✗ No results found for '{location_name}'")
                    return None
            else:
                print(f"✗ API error: {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"✗ Network error: {e}")
            return None
        except Exception as e:
            print(f"✗ Unexpected error: {e}")
            return None
    
    def reverse_geocode(self, latitude, longitude):
        """Convert coordinates back to location name"""
        try:
            reverse_url = "https://nominatim.openstreetmap.org/reverse"
            params = {
                'lat': latitude,
                'lon': longitude,
                'format': 'json',
                'addressdetails': 1
            }
            
            response = requests.get(
                reverse_url, 
                params=params, 
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                
                if 'display_name' in result:
                    return {
                        'display_name': result['display_name'],
                        'city': result.get('address', {}).get('city', ''),
                        'state': result.get('address', {}).get('state', ''),
                        'country': result.get('address', {}).get('country', '')
                    }
            
            return None
            
        except Exception as e:
            print(f"Reverse geocoding error: {e}")
            return None

# Demonstrate geocoding functionality
geocoder = SimpleGeocoder()

print("\nGeocoding Demonstration:")
print("=" * 40)

# Test geocoding various locations
test_locations = [
    "New York, NY",
    "London, UK",
    "Tokyo, Japan",
    "InvalidCityName12345",
    "San Francisco, CA"
]

location_results = {}

for location in test_locations:
    result = geocoder.geocode_location(location)
    if result:
        location_results[location] = result
        print(f"\n{location}:")
        print(f"  Coordinates: ({result['latitude']:.4f}, {result['longitude']:.4f})")
        print(f"  Full name: {result['display_name']}")
    else:
        print(f"\n{location}: Could not geocode")

# Demonstrate reverse geocoding
print("\nReverse Geocoding Demonstration:")
print("=" * 40)

# Test reverse geocoding
test_coords = [
    (40.7128, -74.0060),  # New York City
    (51.5074, -0.1278),   # London
    (35.6762, 139.6503)   # Tokyo
]

for lat, lon in test_coords:
    reverse_result = geocoder.reverse_geocode(lat, lon)
    if reverse_result:
        print(f"({lat}, {lon}) → {reverse_result['display_name']}")
    else:
        print(f"({lat}, {lon}) → Could not reverse geocode")

