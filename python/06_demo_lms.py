import json
import os
from datetime import datetime

class WeatherLocationManager:
    """Complete location management for weather applications"""
    
    def __init__(self, data_file="user_locations.json"):
        self.data_file = data_file
        self.validator = LocationValidator()
        self.geocoder = SimpleGeocoder()
        self.autocomplete = LocationAutocomplete()
        
        # User location data
        self.user_data = {
            'default_location': None,
            'favorite_locations': [],
            'search_history': [],
            'location_cache': {},
            'user_preferences': {
                'units': 'imperial',
                'max_history': 20,
                'auto_save': True,
                'show_coordinates': False
            }
        }
        
        # Load existing user data
        self.load_user_data()
    
    def load_user_data(self):
        """Load user location data from file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    saved_data = json.load(f)
                    self.user_data.update(saved_data)
                print(f"✓ Loaded user location data from {self.data_file}")
        except Exception as e:
            print(f"Could not load user data: {e}")
            print("Starting with fresh user data")
    
    def save_user_data(self):
        """Save user location data to file"""
        try:
            if self.user_data['user_preferences']['auto_save']:
                with open(self.data_file, 'w') as f:
                    json.dump(self.user_data, f, indent=2)
                print(f"✓ Saved user location data to {self.data_file}")
        except Exception as e:
            print(f"Could not save user data: {e}")
    
    def set_default_location(self, location_input):
        """Set user's default location for weather"""
        # Process the location
        result = self.process_location_input(location_input)
        
        if result['success']:
            location_data = result['location_data']
            self.user_data['default_location'] = {
                'name': location_data['display_name'],
                'short_name': location_data.get('short_name', location_data['display_name']),
                'latitude': location_data['latitude'],
                'longitude': location_data['longitude'],
                'set_date': datetime.now().isoformat()
            }
            
            self.save_user_data()
            print(f"✓ Default location set to: {self.user_data['default_location']['short_name']}")
            return True
        else:
            print(f"✗ Could not set default location: {result['error']}")
            return False
    
    def add_favorite_location(self, location_input):
        """Add a location to user's favorites"""
        result = self.process_location_input(location_input)
        
        if result['success']:
            location_data = result['location_data']
            
            # Check if already in favorites
            for favorite in self.user_data['favorite_locations']:
                if favorite['short_name'] == location_data.get('short_name', location_data['display_name']):
                    print(f"'{location_data['display_name']}' is already in favorites")
                    return False
            
            # Add to favorites
            favorite = {
                'name': location_data['display_name'],
                'short_name': location_data.get('short_name', location_data['display_name']),
                'latitude': location_data['latitude'],
                'longitude': location_data['longitude'],
                'added_date': datetime.now().isoformat()
            }
            
            self.user_data['favorite_locations'].append(favorite)
            self.save_user_data()
            print(f"✓ Added '{favorite['short_name']}' to favorites")
            return True
        else:
            print(f"✗ Could not add to favorites: {result['error']}")
            return False
    
    def get_location_for_weather(self, location_input=None):
        """
        Get location data ready for weather API calls
        
        Args:
            location_input: User's location request, or None for default location
            
        Returns:
            dict with weather-ready location data
        """
        if location_input is None:
            # Use default location
            if self.user_data['default_location']:
                default = self.user_data['default_location']
                return {
                    'success': True,
                    'location_data': {
                        'name': default['short_name'],
                        'latitude': default['latitude'],
                        'longitude': default['longitude'],
                        'source': 'default_location'
                    }
                }
            else:
                return {
                    'success': False,
                    'error': 'No default location set. Please specify a location.',
                    'suggestion': 'Set a default location with set_default_location()'
                }
        
        # Process user input
        result = self.process_location_input(location_input)
        
        if result['success']:
            # Add to search history
            self._add_to_search_history(result['location_data'])
            
            return {
                'success': True,
                'location_data': {
                    'name': result['location_data'].get('short_name', result['location_data']['display_name']),
                    'latitude': result['location_data']['latitude'],
                    'longitude': result['location_data']['longitude'],
                    'source': 'user_input'
                }
            }
        else:
            return result
    
    def process_location_input(self, location_input):
        """Process any location input through the complete pipeline"""
        # Step 1: Validate input
        cleaned, validation_msg = self.validator.clean_location_input(location_input)
        if not cleaned:
            return {'success': False, 'error': validation_msg}
        
        # Step 2: Check cache
        cache_key = cleaned.lower()
        if cache_key in self.user_data['location_cache']:
            cached = self.user_data['location_cache'][cache_key]
            return {'success': True, 'location_data': cached, 'source': 'cache'}
        
        # Step 3: Geocode
        geocode_result = self.geocoder.geocode_location(cleaned)
        if not geocode_result:
            return {
                'success': False, 
                'error': f"Could not find location '{cleaned}'",
                'suggestions': [
                    "Check spelling",
                    "Try including state or country",
                    "Use a major city name"
                ]
            }
        
        # Step 4: Prepare location data
        location_data = {
            'original_input': location_input,
            'cleaned_input': cleaned,
            'display_name': geocode_result['display_name'],
            'short_name': self._create_short_display_name(geocode_result),
            'latitude': geocode_result['latitude'],
            'longitude': geocode_result['longitude'],
            'type': geocode_result['type']
        }
        
        # Step 5: Cache the result
        self.user_data['location_cache'][cache_key] = location_data
        self.save_user_data()
        
        return {'success': True, 'location_data': location_data, 'source': 'geocoding'}
    
    def _create_short_display_name(self, geocode_result):
        """Create a short display name from geocoding result"""
        display_name = geocode_result['display_name']
        parts = display_name.split(',')
        
        # Try to create "City, State" or "City, Country" format
        if len(parts) >= 3:
            return f"{parts[0].strip()}, {parts[-2].strip()}"
        elif len(parts) >= 2:
            return f"{parts[0].strip()}, {parts[1].strip()}"
        else:
            return parts[0].strip()
    
    def _add_to_search_history(self, location_data):
        """Add location to search history"""
        # Remove if already in history
        history = self.user_data['search_history']
        history = [item for item in history if item['short_name'] != location_data.get('short_name')]
        
        # Add to beginning of history
        history_item = {
            'short_name': location_data.get('short_name', location_data['display_name']),
            'display_name': location_data['display_name'],
            'latitude': location_data['latitude'],
            'longitude': location_data['longitude'],
            'search_date': datetime.now().isoformat()
        }
        
        history.insert(0, history_item)
        
        # Limit history size
        max_history = self.user_data['user_preferences']['max_history']
        self.user_data['search_history'] = history[:max_history]
    
    def get_user_summary(self):
        """Get a summary of user's location data"""
        summary = {
            'default_location': self.user_data['default_location']['short_name'] if self.user_data['default_location'] else None,
            'favorite_count': len(self.user_data['favorite_locations']),
            'history_count': len(self.user_data['search_history']),
            'cache_count': len(self.user_data['location_cache'])
        }
        return summary
    
    def clear_cache(self):
        """Clear location cache"""
        self.user_data['location_cache'] = {}
        self.save_user_data()
        print("✓ Location cache cleared")
    
    def clear_history(self):
        """Clear search history"""
        self.user_data['search_history'] = []
        self.save_user_data()
        print("✓ Search history cleared")

# Demonstrate complete location management
print("\nComplete Location Management Demonstration:")
print("=" * 50)

# Create location manager
location_manager = WeatherLocationManager(data_file="demo_user_locations.json")

# Set default location
print("\n1. Setting default location:")
location_manager.set_default_location("Chicago, IL")

# Add some favorites
print("\n2. Adding favorite locations:")
location_manager.add_favorite_location("New York, NY")
location_manager.add_favorite_location("London, UK")

# Get weather-ready location data
print("\n3. Getting location for weather API:")

# Test with default location
result = location_manager.get_location_for_weather()
if result['success']:
    loc = result['location_data']
    print(f"Default location: {loc['name']} at ({loc['latitude']:.4f}, {loc['longitude']:.4f})")

# Test with user input
result = location_manager.get_location_for_weather("Tokyo, Japan")
if result['success']:
    loc = result['location_data']
    print(f"User input location: {loc['name']} at ({loc['latitude']:.4f}, {loc['longitude']:.4f})")

# Show user summary
print("\n4. User Location Summary:")
summary = location_manager.get_user_summary()
for key, value in summary.items():
    print(f"  {key.replace('_', ' ').title()}: {value}")

print("\n5. User location data saved to 'demo_user_locations.json'")
